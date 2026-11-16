# modal-hermes

A [Hermes Agent](https://github.com/NousResearch/hermes-agent) model-provider
plugin for [Modal](https://modal.com/?utm_source=hermes-agent&utm_medium=referral&utm_campaign=inference_partners&utm_content=readme).

## Setup

1. Install the plugin:

   ```sh
   hermes plugins install modal
   ```

   You'll be prompted to create a [proxy token](https://modal.com/docs/guide/webhook-proxy-auth?utm_source=hermes-agent&utm_medium=referral&utm_campaign=inference_partners&utm_content=readme), which you can create via the [dashboard](https://modal.com/settings/proxy-auth-tokens?utm_source=hermes-agent&utm_medium=referral&utm_campaign=inference_partners&utm_content=readme) or [CLI](https://modal.com/docs/cli/latest/workspace#modal-workspace-proxy-tokens?utm_source=hermes-agent&utm_medium=referral&utm_campaign=inference_partners&utm_content=readme).

2. Select Modal as the model provider:

   ```sh
   hermes model
   ```

	Optionally, you can override `MODAL_BASE_URL`; for e.g., when using a [Dedicated Endpoint](https://modal.com/docs/guide/dedicated-endpoints?utm_source=hermes-agent&utm_medium=referral&utm_campaign=inference_partners&utm_content=readme) of the form
	`https://<workspace>-<env>--<app>.<region>.modal.direct/v1`.
