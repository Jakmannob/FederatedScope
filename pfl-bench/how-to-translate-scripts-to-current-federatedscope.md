# How to translate the old pFL-Bench configs to current FederatedScope

The example configs in the `yaml_best_runs_example` folder in the current version of FederatedScope are just copied from the pFL-Bench branch. Therefore any changes here can be applied to any pFL-Bench configs.

## `cfg.asyn`
- `cfg.asyn.timeout` is now called `cfg.asyn.time_budget`

## `cfg.attack`
- `cfg.attack.alpha_prop_loss` is deprecated and defaults to $0$ anyway. Remove field from all config files.
- Since all other fields in `cfg.attack` are also just defaults, remove the whole section.

## `cfg.cfg_file`
- Remove the field `cfg.cfg_file`.

## `cfg.data`
- [ ] Check, if `cfg.data.transform` is still working.
- `cfg.data.graphsaint` is removed and child fields are placed one order up, i.e. move `cfg.data.graphsaint.num_steps` to `cfg.data.num_steps` and `cfg.data.graphsaint.walk_length` to `cfg.data.walk_length`
- `cfg.data.batch_size` will be removed in the future and replaced by `cfg.dataloader.batch_size`. Move it now already.

## `cfg.early_stop`
- Drop `cfg.early_stop.the_smaller_the_better`. It's been replaced with `the_larger_the_better`, which is however implied by the loss, and not configurable anymore.

## `cfg.federate`
- `cfg.federate.batch_or_epoch` was split and moved to `cfg.finetune.batch_or_epoch` and `cfg.train.batch_or_epoch`. Remove from `cfg.federate` and place in `cfg.finetune` and `cfg.train`.
- `cfg.federate.local_update_steps` was moved to `cfg.finetune.batch_or_epoch` and `cfg.train.batch_or_epoch`. Remove from `cfg.federate` and place in `cfg.finetune` and `cfg.train`.
- `cfg.federate.sample_client_rate` and `cfg.federate.sample_client_num` should not both be specified at the same time. Decide on one (I decide on `cfg.federate.sample_client_num`).

### `cfg.federate.local_update_steps`
- Somehow, `local_update_steps` is set twice, one time directly in the lowest indentation, with `federate.local_update_steps`. Remove this also.

## `cfg.fedsageplus`
- `cfg.fedsageplus.[a-c]` were changed from `int` to `float`. Adjust by setting to `1.` instead of `1`.

## `cfg.hpo`

- `cfg.hpo.scheduler`: The scheduler `bruteforce` is was removed. I currently have no idea, with which one I should replace it with.
- [ ] Find out, which scheduler replaces `bruteforce`. In the mean time, replace it with `sha`.
- `cfg.hpo.init_strategy` was removed. Delete the field.
- `cfg.hpo.log_scale` was removed. Delete the field.
- `cfg.hpo.plot_interval` was removed. Delete the field.

### `cfg.hpo.fedex`
- `cfg.hpo.fedex.num_arms` was removed. Delete the field.

### `cfg.hpo.sha`
- `cfg.hpo.sha.elim_round_num` was removed. Delete the field.

### `cfg.hpo.pbt`
- `cfg.hpo.pbt` was removed. Delete the field and all childs.

## `cfg.optimizer`
- `cfg.optimizer` was moved one layer down. Move it and all of its childs to `cfg.train` and `cfg.finetune`.
- `cfg.optimizer.grad_clip` was moved to `cfg.grad.grad_clip`.

### `cfg.optimizer.lr`
- Somehow, `lr` is set twice, one time directly in the lowest indentation, with `optimizer.lr`. Remove this also.

## `cfg.personalization.regular_weight`
- Somehow, `regular_weight` is set twice, one time directly in the lowest indentation, with `personalization.regular_weight`. Remove this also.

## `cfg.trainer`
- `cfg.trainer` was removed.
- `cfg.trainer.finetune.freeze_param` was removed. Delete the field.
- `cfg.trainer.finetune.lr` was moved to `cfg.finetune.optimizer.lr`. Move the field.
- `cfg.trainer.finetune.before_eval` was moved to `cfg.finetune.before_eval`. Move the field.
- `cfg.trainer.finetune.steps` was moved to `cfg.finetune.local_update_steps`. Move the field.
- `cfg.trainer.type` was removed. The type is assigned automatically now (or at least that's what I think...). Remove the field.
