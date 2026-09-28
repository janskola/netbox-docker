# Local fork notes — netbox-docker

This repo is a fork of netbox-community/netbox-docker
(https://github.com/netbox-community/netbox-docker), used as a git
submodule in the main infra repo at compose/netbox-docker. It carries
local customizations on top of upstream and is set up to keep pulling
in upstream updates over time.

## Remotes

- origin   -> git@github.com:janskola/netbox-docker.git
             (your fork, where local customizations live and get pushed)
- upstream -> https://github.com/netbox-community/netbox-docker.git
             (the original project, pulled from to stay current)

Check anytime with:

    git remote -v

## Local customizations (as of the initial fork)

- configuration/plugins.py  — modified: enables netbox_diode_plugin + netbox_dns
- Dockerfile-custom         — added
- plugin_requirements.txt   — added

These live as regular commits on the release branch, on top of
upstream's history.

### netbox_diode_plugin config

`configuration/plugins.py` sets `diode_target_override` (just a hostname, fine to commit) but reads
`netbox_to_diode_client_secret` from the `NETBOX_TO_DIODE_CLIENT_SECRET` env var — **never hardcode that secret
here**, this fork is public. Supply it via `docker-compose.override.yml` (gitignored):

    services:
      netbox:
        environment:
          NETBOX_TO_DIODE_CLIENT_SECRET: "<secret>"
      netbox-worker:
        environment:
          NETBOX_TO_DIODE_CLIENT_SECRET: "<secret>"

This must be the same secret registered for the `netbox-to-diode` OAuth2 client in
[`../diode-docker/`](../diode-docker/README.md)'s Hydra instance (`oauth2/client/client-credentials.json` there).
If you rotate one side, rotate both and restart `diode-auth-bootstrap` + this stack's `netbox`/`netbox-worker`.

## Pulling in upstream updates

    git fetch upstream
    git merge upstream/release

- If upstream hasn't touched the same lines you customized, this
  merges cleanly.
- If there's a conflict (e.g. upstream also edited
  configuration/plugins.py), git will flag it. Resolve manually,
  keeping your customizations, then:

    git add <resolved-file>
    git commit

- Push the merged result to your fork:

    git push origin release

Rebase is an alternative to merge (git rebase upstream/release) for
linear history, but needs conflict resolution on every rebase plus a
force-push (git push --force-with-lease origin release) afterward.
Stick with merge unless you have a specific reason not to.

## Updating the submodule pointer in the main repo

After pulling/pushing changes here, go back to the parent repo and
commit the new commit hash:

    cd ../..
    git add compose/netbox-docker
    git commit -m "Update netbox-docker submodule"

## Cloning the main repo fresh

Submodules aren't checked out by a plain git clone. Use:

    git clone --recurse-submodules <main-repo-url>

or, if already cloned:

    git submodule update --init --recursive

## Security note

This fork is PUBLIC on GitHub. Before pushing any new customization,
double-check it doesn't contain secrets (API keys, tokens, internal
hostnames/IPs, credentials in URLs). .env is already gitignored —
keep it that way, and keep actual secrets out of
configuration/plugins.py, Dockerfile-custom, and
plugin_requirements.txt.
