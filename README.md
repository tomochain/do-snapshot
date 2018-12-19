# goutte
DigitalOcean snapshot automation.

## Why
DigitalOcean doesn't propose any way of automating snapshots.
There is some SaaS that can take care of that but paying for executing some API requests seemed a bit off.

That why we developed a simple script that you can run with cron jobs or in a build service like Travis for free.

## Requirements
- Python ^3.6
- A DigitalOcean account

## Installation
Install it directly from pip:
```bash
pip3 install --user goutte
```

## Configuration file
Goutte takes its configuration from a pretty straightforward toml file.
We provided and example in `goutte.example.toml`.

```toml
retention = 10     # Number of backups to keep

[droplets]
names = [          # Array of droplets names you want to snapshot
  'server01',
  'server02',
  'server03',
]

[volumes]
names = [          # Array of volumes names you want to snapshot
  'db01',
  'redis01',
  'redis02',
]
```

## Usage
Goutte takes two arguments who can also be set via environment variables:

| # | Help     | Description                         | Environment variable |
| - | -------- | ----------------------------------- | -------------------- |
| 1 | CONFIG   | Path to the toml configuration file | `GOUTTE_CONFIG`      |
| 2 | DO_TOKEN | Your DigitalOcean API token         | `GOUTTE_DO_TOKEN`    |

```bash
$ goutte --help
Usage: goutte [OPTIONS] CONFIG DO_TOKEN

  DigitalOcean snapshot automation service

Options:
  --debug    Enable debug logging
  --version  Show the version and exit.
  --help     Show this message and exit.
```

## Run with Docker
We have a Docker image ready for you to use on Docker Hub.
It will read by default the configuration under `/goutte/goutte.toml`

```bash
docker run \
  -e GOUTTE_DO_TOKEN=${do_token} \
  -v $(pwd)/goutte.toml:/goutte/goutte.toml \
  tomochain:goutte
```

## Automating
You can easily automate it via cron job or by leveraging free CI tools like Travis.
We provided and example travis configuration in `travis.example.yml`.

TODO
