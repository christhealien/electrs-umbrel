# electrs-umbrel

Electrs for Umbrel in the blake2b look (black, white and grey, like Blake2b ASIC Control, DATUM Gateway and Mempool).

- `blake2b-electrs/`: the Umbrel app folder (manifest, compose, Tor, icon). Same ports, IP and Tor service as Horizon's
  `btc-electrs`, so wallets and Mempool keep working; do not run both at once.
- The Electrs server is Horizon's image (`ghcr.io/horizon-btc/electrs`, pinned in the compose file). This repo only
  rebuilds the **connection page** (`ghcr.io/christhealien/blake2b-electrs-ui`) from retropex/umbrel-electrs
  (`UI_REF`) with `overlay/ui/blake2b-theme.css`, the icon and a new title applied by `tools/patch_ui.py`.

Release: bump the version in `blake2b-electrs/umbrel-app.yml` and the image tag in `blake2b-electrs/docker-compose.yml`,
then `git tag electrs-vX.Y.Z && git push origin master electrs-vX.Y.Z`. The workflow builds amd64 and arm64 images and
(with the `STORE_TOKEN` secret) copies the app folder into the store. Make the ghcr package public once.
