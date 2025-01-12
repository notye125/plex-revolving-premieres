# trakt_list_item_manager
### How It Works

This script is part of a larger workflow to manage and maintain TV show collections using various tools. Below is a breakdown of how it integrates:

1. **Trakt List (Series Premiers)**:
    - Manually add upcoming series premieres to a Trakt list.

2. **Kometa**:
    - Syncs with the Trakt list to create a Plex collection called "Series Premiers - 90 Day Trials."
    - Sends new items to Sonarr with the tag `trakt-premier`.

    > **Kometa YAML**: An example configuration for Kometa is included in the repository. [View here](kometa-trakt-list-config.yaml).

3. **Sonarr**:
    - Downloads episodes and adds them to Plex, tagging them with `trakt-premier`.

4. **Maintainerr**:
    - Monitors shows tagged with `trakt-premier` and adds them to the "90-Day Rolling Delete" collection.
    - Automatically deletes unwatched shows older than 90 days.

    > **Maintainerr YAML**: An example configuration for Maintainerr is included in the repository. [View here](maintainerr_premiers_rules_.yaml).

5. **This Script**:
    - Runs daily to check the Trakt list.
    - Removes shows that have aired more than 90 days ago, based on data from TMDb.

6. **Kometa Collection**:
    - Always displays the freshest series premieres (aired within 90 days), whether watched or unwatched.
