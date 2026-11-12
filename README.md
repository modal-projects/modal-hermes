# modal-hermes

A [Hermes Agent](https://github.com/NousResearch/hermes-agent) model-provider
plugin for [Modal](https://modal.com).

## Setup

1. Create a Modal proxy token:

   ```sh
   modal workspace proxy-tokens create
   modal workspace proxy-tokens allow <token-id> <environment>
   ```

   This yields a combined `wk-<id>.ws-<secret>` token.

2. Save it — either in `~/.hermes/.env` or the process environment:

   ```sh
   MODAL_PROXY_TOKEN=wk-<id>.ws-<secret>
   ```

   Optional: `MODAL_BASE_URL` selects another shared-gateway region or a
   dedicated endpoint, e.g.
   `https://<workspace>-<env>--<app>.<region>.modal.direct/v1`. Default is
   `https://inference.us-west.modal.direct/v1`.

3. Select Modal in Hermes: `hermes model` → Modal (provider: `modal`).
