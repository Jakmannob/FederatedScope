import os
import yaml


class ConfigFileTranslator():
    
    def __init__(self):
        pass

    def translate_file(self, old_path, new_path, new_name=None,
            wandb_user_name=None):
        """Translates an old config file into a config file, that the current
        FederatedScope version will be able to parse

        Args:
            old_path (str): The path to the old configuration file
            new_path (str): The path to the folder, where the new configuration
                file will be saved to.
            new_name (str, optional): Filename of the new configuration file.
                Reuses the old filename, if set to None. Defaults to None.
            wandb_user_name (str, optional): This will set your user name on
                weights and biases, if not None. Defaults to None.
        """
        config = self.load_old_config_file(old_path)
        if new_name == None:
            new_name = os.path.split(old_path)[-1]
        new_path = os.path.join(new_path, new_name)

        # Following the instructions from how-to-translate-[...].md
        # 1. Create missing sections
        if not 'dataloader' in config:
            config['dataloader'] = dict()
        if not 'finetune' in config:
            config['finetune'] = dict()
            config['finetune']['optimizer'] = dict()
        if not 'grad' in config:
            config['grad'] = dict()
        if not 'train' in config:
            config['train'] = dict()

        # 2. Follow translation rules
        if 'asyn' in config:
            if 'timeout' in config['asyn']:
                config['asyn']['time_budget'] = config['asyn'].pop('timeout')

        if 'attack' in config:
            config.pop('attack')

        if 'cfg_file' in config:
            config.pop('cfg_file')

        if 'data' in config:
            if 'graphsaint' in config['data']:
                for key, value in config['data']['graphsaint'].items():
                    config['data'][key] = value
                config['data'].pop('graphsaint')
            if 'batch_size' in config['data']:
                config['dataloader']['batch_size'] = config['data'].\
                    pop('batch_size')

        if 'early_stop' in config:
            if 'the_smaller_the_better' in config['early_stop']:
                config['early_stop'].pop('the_smaller_the_better')

        if 'federate' in config:
            if 'batch_or_epoch' in config['federate']:
                config['train']['batch_or_epoch'] = config['federate'].\
                    pop('batch_or_epoch')
            if 'local_update_steps' in config['federate']:
                config['train']['local_update_steps'] = config['federate'].\
                    pop('local_update_steps')
            if 'sample_client_rate' and 'sample_client_num' in\
                config['federate']:
                config['federate'].pop('sample_client_rate')

        if 'federate.local_update_steps' in config:
            config.pop('federate.local_update_steps')

        if 'fedsageplus' in config:
            for letter in ['a', 'b', 'c']:
                if letter in config['fedsageplus']:
                    config['fedsageplus'][letter] =\
                        float(config['fedsageplus'][letter])

        if 'hpo' in config:
            if 'scheduler' in config['hpo']:
                if config['hpo']['scheduler'] == 'bruteforce':
                    config['hpo']['scheduler'] = 'sha'
            if 'init_strategy' in config['hpo']:
                config['hpo'].pop('init_strategy')
            if 'log_scale' in config['hpo']:
                config['hpo'].pop('log_scale')
            if 'plot_interval' in config['hpo']:
                config['hpo'].pop('plot_interval')
            if 'fedex' in config['hpo']:
                if 'num_arms' in config['hpo']['fedex']:
                    config['hpo']['fedex'].pop('num_arms')
            if 'sha' in config['hpo']:
                if 'elim_round_num' in config['hpo']['sha']:
                    config['hpo']['sha'].pop('elim_round_num')
            if 'pbt' in config['hpo']:
                config['hpo'].pop('pbt')
        
        if 'optimizer' in config:
            if 'grad_clip' in config['optimizer']:
                config['grad']['grad_clip'] = config['optimizer'].\
                    pop('grad_clip')
            config['train']['optimizer'] = config.pop('optimizer')

        if 'optimizer.lr' in config:
            config.pop('optimizer.lr')

        if 'personalization.regular_weight' in config:
            config.pop('personalization.regular_weight')
        
        if 'trainer' in config:
            if 'finetune' in config['trainer']:
                if 'lr' in config['trainer']['finetune']:
                    config['finetune']['optimizer']['lr'] = \
                        config['trainer']['finetune'].pop('lr')
                if 'before_eval' in config['trainer']['finetune']:
                    config['finetune']['before_eval'] = \
                        config['trainer']['finetune'].pop('before_eval')
                if 'steps' in config['trainer']['finetune']:
                    config['finetune']['local_update_steps'] = \
                        config['trainer']['finetune'].pop('steps')
            config.pop('trainer')
        
        # 3. Set wandb username, if specified
        if wandb_user_name != None:
            if 'wandb' in config:
                if 'name_user' in config['wandb']:
                    config['wandb']['name_user'] = wandb_user_name

        self.save_new_config_file(new_path, config)

    def load_old_config_file(self, old_path):
        with open(old_path, "r") as stream:
            try:
                return yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)
                exit()

    def save_new_config_file(self, new_path, config):
        with open(new_path, 'w') as outfile:
            yaml.dump(config, outfile, default_flow_style=False)
