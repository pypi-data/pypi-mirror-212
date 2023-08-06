from transformers import get_linear_schedule_with_warmup
import torch
import numpy as np
import pandas as pd
from torch import nn, optim
from datetime import datetime
from sklearn.metrics import precision_score, recall_score, f1_score
import logging
from rich.progress import Progress, SpinnerColumn, TextColumn, MofNCompleteColumn, BarColumn, TimeElapsedColumn, TimeRemainingColumn


WORKER = 'TRAINER'


_EVAL_FUNCTIONS = {
    'f1': f1_score,
    'precision': precision_score,
    'recall': recall_score
}


class Trainer:
    """
    Trainer - can train pytorch model based on Dataset and Model passed in

    Params:
        device => torch.cuda.device: primary device to put model and data on
    
    """


    def __init__(self, 
                 device: torch.cuda.device
                 ):
        self.device = device
        logging.info(f'{WORKER}: Trainer initialized on {device}') 

    def _get_loss_pred(self, outputs, labels, loss_fn, threshold, binary):
        """
        get loss and prediction from output of NN
        
        Args:
            outputs: output from model()
            binary: True or False
            loss_fn: loss function
            threshold: threshold to give a positive prediction (only for binary now)
        
        Returns:
            loss: pytorch loss
            preds: list of predicted labels
            
        """
        if binary: # if doing binary classification
            outputs = outputs.squeeze()
            loss = loss_fn(outputs, labels)
            preds_proba = np.array(torch.sigmoid(outputs).tolist()) # add sigmoid since no sigmoid in NN
            preds = np.where(preds_proba > threshold, 1, 0)
            return loss, preds, preds_proba, [1-preds_proba, preds_proba]
        else: # if doing multiclass 
            m = nn.Softmax(dim=1)
            loss = loss_fn(outputs, labels.long())
            # _, preds = torch.max(outputs, dim=1)
            preds_proba, preds = torch.max(m(outputs), dim=1)
            return loss, preds, preds_proba, m(outputs)

    def _eval_model(self, model, data_loader, loss_fn, device, threshold = 0.5, binary = True):
        model.eval()
        losses = []
        preds_l = []
        preds_probas_l = []
        true_labels_l = []
        with torch.no_grad():
            for d in data_loader:
                input_ids = d["input_ids"].to(device)
                attention_mask = d["attention_mask"].to(device)
                labels = d["labels"].to(device)
                # labels = torch.nn.functional.one_hot(labels.to(torch.int64)).to(device).to(float) # one hot label to the right shape

                outputs = model(
                                input_ids=input_ids,
                                attention_mask=attention_mask
                                )

                loss, preds, preds_probas, preds_probas_all = self._get_loss_pred(outputs, labels, loss_fn, threshold, binary)
            
                preds_l.extend(preds.tolist())
                true_labels_l.extend(labels.tolist())
                preds_probas_l.extend(preds_probas.tolist())
                
                losses.append(loss.item())
                
        preds_l = np.array(preds_l)
        true_labels_l = np.array(true_labels_l)
        preds_probas_l = np.array(preds_probas_l)
        
        return preds_l, preds_probas_l, true_labels_l, losses

    def _evaluate_by_metrics(self, y_true, y_pred, metrics_list, average = 'binary', log=False):

        """
        Helper function that prints out and save a list of metrics defined by the user
        """
        results = {}
        output_str = ''

        for metric_name in metrics_list:
            metric_func = _EVAL_FUNCTIONS[metric_name]

            if metric_name == 'confusion_matrix':
                score = metric_func(y_true, y_pred)
                score = score.tolist()
                output_str += f'| {metric_name}: {score} '
                results[metric_name] = score
            else:
                score = metric_func(y_true, y_pred, average=average, zero_division=0)
                results[metric_name] = score

                if type(score) == float:
                    score = round(score, 4)

                output_str += f'| {metric_name}: {score} '
        if log:
            logging.info(f'{WORKER} {log}: {output_str}')
        return results

    def train(self, 
              ModelModule,
              TrainDataModule,
              ValDataModule,
              params,
              eval_config = {
                "focused_indexes": None,
                "save_metric": 'f1',
                "multiclass_average": "weighted",
                "eval_freq": 1,
                "watch_list": ["f1", "precision", "recall"]
              },
              early_stopping = None,
                                ):
        """
        function that trains the model

        Params:
            ModelModule => PytorchNlpModel Object
            TrainDataModule => Dataset Object
            ValDataModule =? Dataset Object
            params => dict like
            eval_config => dict like
            early_stopping => int or None
        
        Returns
            model => PytorchNlpModel
            model_info => dict
        """    
    
        ## set up data 
        binary =TrainDataModule.binary
        indexes_to_labels = TrainDataModule.indexes_to_labels
        label_col = TrainDataModule.label_col
        threshold = 0
        df_train = TrainDataModule.df
        
        # unpack variables in config
        watch_list = eval_config['watch_list']
        save_metric_func = _EVAL_FUNCTIONS[eval_config['save_metric']]
        multiclass_average = eval_config['multiclass_average']
        eval_freq = eval_config['eval_freq']
        best_val_score = 0
        focused_indexes = eval_config['focused_indexes']

        # Checking for Binary or Multiclass
        if binary: # binary
            RATIO = df_train[df_train[label_col] == 0].shape[0] / df_train[df_train[label_col] == 1].shape[0]
            loss_fn = nn.BCEWithLogitsLoss(
                                        pos_weight = torch.tensor(RATIO )
                                        ).to(self.device)
            focused_indexes = None
            threshold = 0.5
        else: # multiclassfication
            ## Assign class weights
            class_weight = [] 
            sample = df_train[label_col].value_counts().to_dict()

            for label in indexes_to_labels:
                class_weight.append(max(sample.values()) / sample[label])
            if focused_indexes: # if focused index boost their weights 
                for index in focused_indexes:
                    class_weight[index] = class_weight[index] * float(params.get('boost', 1))
            loss_fn = nn.CrossEntropyLoss(
                                                weight = torch.tensor(class_weight).to(self.device)
                                                ).to(self.device)

        # load tokenizer and model
        tokenizer = ModelModule.tokenizer 

        # enable multiple GPU training
        model = ModelModule
        if torch.cuda.device_count() > 1:
            num_gpus = torch.cuda.device_count()
            logging.info(f'{WORKER}: Detected {num_gpus} GPUs, utilizing all for training...')
            model = nn.DataParallel(model)    ##multiple GPU Training
    
            
        model = model.to(self.device)

        train_data_loader = TrainDataModule.create_data_loader(tokenizer)
        val_data_loader = ValDataModule.create_data_loader(tokenizer)

        # get list eval steps based on eval_freq
        epoch_steps = len(train_data_loader)
        total_steps = epoch_steps * params['EPOCHS']
        total_evaluations = eval_freq * params['EPOCHS']
        logging.info(f'{WORKER}: Total Training Steps: {total_steps}') 
        eval_steps = [int(total_steps/total_evaluations) * i for i in range(1, total_evaluations)]
        eval_steps.append(total_steps)
        logging.info(f'{WORKER}: Eval at steps: {eval_steps}')

        optimizer = optim.AdamW(model.parameters(), lr=params['lr'], weight_decay = params['weight_decay']) # optimizer to update weights
        scheduler = get_linear_schedule_with_warmup(
                                                    optimizer,
                                                    num_warmup_steps=params['warmup_steps'],
                                                    num_training_steps=total_steps
        )

        global_step = 1
        eval_ind = 0
        val_losses_list = [] # record val loss every eval step -> for early stopping
        running_train_loss = 0
        patience_count = 0
        val_scores_list = []
        best_model, best_model_info = None, None

         # start training
        EPOCHS = params['EPOCHS']
        for epoch in range(EPOCHS):

            logging.info(f'{WORKER}: Training Epoch {epoch + 1}/{EPOCHS} ...')

            losses = []
            train_preds_l = []
            train_true_labels_l = []
            
            # training through the train_data_loader
            progress = Progress(SpinnerColumn(spinner_name='line'), 
                            TextColumn("Training ..."),
                            '(',
                            MofNCompleteColumn(),
                            ')',
                            TimeElapsedColumn(),
                            BarColumn(),
                            TimeRemainingColumn(),
                            transient=True)
            with progress:
                task = progress.add_task("Training ...", total=len(train_data_loader))
                for d in train_data_loader:
                    model.train()

                    input_ids = d["input_ids"].to(self.device)
                    attention_mask = d["attention_mask"].to(self.device)
                    labels = d["labels"].to(self.device) 

                    # getting output on current weights
                    outputs = model(
                                    input_ids=input_ids,
                                    attention_mask=attention_mask
                                )

                    # getting loss and preds for the current batch
                    loss, preds, preds_proba, preds_proba_all = self._get_loss_pred(outputs, labels, loss_fn, threshold, binary)

                    # backprogogate and update weights/biases
                    losses.append(loss.item())
                    loss.backward()
                    nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
                    optimizer.step()
                    scheduler.step()
                    optimizer.zero_grad()

                    # record performance
                    running_train_loss += loss.item() # update running train loss
                    train_preds_l.extend(preds.tolist())
                    train_true_labels_l.extend(labels.tolist())

                    # evaluating based on step
                    if global_step == eval_steps[eval_ind]:
                        STEP_INFO = f'[EPOCH {epoch}][EVAL {eval_ind}]'
                        logging.info(f'{WORKER} {STEP_INFO}: Evaluateing at Step {global_step}....')
                        eval_ind += 1
                        val_preds, val_preds_probas, val_trues, val_losses = self._eval_model(
                                                                                                model,
                                                                                                val_data_loader,
                                                                                                loss_fn,
                                                                                                self.device,
                                                                                                threshold,
                                                                                                binary
                                                                                                        )
                        val_score_by_label = {}

                        if binary:
                            average = 'binary'
                        else:
                            average = multiclass_average

                        if focused_indexes: # if focused_indexes are passed in (multiclass only)
                            eval_results_im = self._evaluate_by_metrics(val_trues, val_preds, watch_list, average = None)
                            val_score_all = save_metric_func(val_trues, val_preds, average=None, zero_division=0)
                            
                            eval_results = {}

                            
                            # Log Score by Focused Indexes
                            for index in focused_indexes:
                                label_name = indexes_to_labels[index]
                                output_str = f'{label_name}     '
                                scores = {}
                                for metric_name in eval_results_im:
                                    score = round(eval_results_im[metric_name][index], 3)
                                    output_str += f'{metric_name}: {score}    '
                                    scores[metric_name] = score
                                
                                eval_results[label_name] = scores
                                    
                                val_score_by_label[indexes_to_labels[index]] = round(val_score_all[index], 3)
                            
                                logging.info(f'{WORKER} {STEP_INFO}: {output_str}')
                                
                            val_score = np.mean(val_score_all[focused_indexes])
                        else: # if not focused index or binary
                            eval_results = self._evaluate_by_metrics(val_trues, val_preds, watch_list, average = average, log = STEP_INFO)
                        
                            val_score = save_metric_func(val_trues, val_preds, average = average)

                        val_scores_list.append(val_score)          
                        val_loss = np.mean(val_losses) # getting average val loss
                        val_losses_list.append(val_loss)

                        logging.info(f'{WORKER} {STEP_INFO}: End of Eval - Val Save Metric Score: {round(val_score, 3)}   Val Loss: {round(val_loss, 4)}')

                        # check if needed to be early stopped: 
                        if early_stopping:
                            if patience_count > early_stopping:
                                if val_scores_list[-1] > val_scores_list[-(early_stopping + 1)]:
                                    print('Early Stopping..')
                                    print('Val F1 List: ', val_scores_list)
                                    return None, None
                        
                            patience_count += 1

                        # if a save path provided, better models will be checkpointed
                        if val_score > best_val_score: # if f1 score better. save model checkpoint                    
                            model_info = {
                                    'val_score': val_score,
                                    'val_loss': float(np.round(np.mean(val_losses), 4)),
                                    'time_generated': datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
                                    'focused_labels':  [indexes_to_labels[x]for x in focused_indexes] if focused_indexes  else [],
                                    'val_score_by_focused_label': val_score_by_label,
                                    'eval_results': eval_results,
                                    'epoch': epoch,
                                    'step': global_step
                                }

                            best_model = model
                            best_model_info = model_info
                            best_val_score = val_score # update best f1 score

                            logging.info(f'{WORKER} {STEP_INFO}: End of Eval - Better Val Score, Updated Checkpoint Model...')

                    global_step += 1 # update training step count 
                
                    progress.advance(task)
        
        return best_model, best_model_info


class Evaluator:
    def __init__(self, ModelModule, device):
        self.ModelModule = ModelModule
        self.device = device
    
    def _eval_model_detailed(self, data_loader, device, binary = True):
        model =  self.ModelModule
        model.eval()
        print('generating detailed evaluation..')
        
        texts_l = []
        preds_l = []
        preds_probas_l = []
        true_labels_l = []
        preds_probas_all_l = []
        
        with torch.no_grad():
            for d in data_loader:
                texts = d['text']
                input_ids = d["input_ids"].to(device)
                attention_mask = d["attention_mask"].to(device)
                labels = d["labels"].to(device)

                outputs = model(
                                input_ids=input_ids,
                                attention_mask=attention_mask
                                )
    
                if binary: # if doing binary classification
                    threshold = 0.5
                    outputs = outputs.squeeze()
                    preds_proba = np.array(torch.sigmoid(outputs).tolist()) # add sigmoid since no sigmoid in NN
                    preds = np.where(preds_proba > threshold, 1, 0)
                    preds_probas_all = [1-preds_proba, preds_proba]
                                            
                else: # if doing multiclass 
                    m = nn.Softmax(dim=1)
                    preds_proba, preds = torch.max(m(outputs), dim=1)
                    preds_probas_all =m(outputs).cpu().tolist()
           
                texts_l.extend(texts)
                preds_l.extend(preds.tolist())
                preds_probas_l.extend(preds_proba.tolist())
                true_labels_l.extend(labels.tolist())
                preds_probas_all_l.extend(preds_probas_all)
                
        return texts_l, preds_l, preds_probas_l, true_labels_l, preds_probas_all_l
    
    def predict_cohort(self, DataModule):
        tokenizer = self.ModelModule.tokenizer
        dataloader = DataModule.create_data_loader(tokenizer)
        texts_l, preds_l, preds_probas_l, true_labels_l, preds_probas_all_l = self._eval_model_detailed(dataloader, 
                                                                                                       self.device, 
                                                                                                       binary = DataModule.binary)
        
        return texts_l, preds_l, preds_probas_l, true_labels_l, preds_probas_all_l