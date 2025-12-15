#!/bin/bash

#SBATCH --partition mit_normal
#SBATCH --output /dev/null
#SBATCH --cpus-per-task=1

source /etc/profile.d/modules.sh  # When run via crontab, this is needed to load the modules
module load miniforge

conda activate /orcd/data/dandi/001/environments/name-dandi+compute_env

cd /orcd/data/dandi/001/all-dandi-compute/blobs-to-paths
python update.py

git add blob_id_to_path.json
git commit --message "update" | true
git push

# CRON
# 0 6 * * * flock -n /orcd/data/dandi/001/flocks/update_blobs_to_paths.lock sbatch /orcd/data/dandi/001/all-dandi-compute/blobs-to-paths/script.sh
