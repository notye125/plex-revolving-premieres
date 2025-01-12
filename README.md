# Plex Revolving Premieres

### This workflow creates a dynamic 'Series Premieres' collection on your Plex Server's home tab, showcasing the latest TV show premieres without clutter or wasted space. The collection automatically updates to include only shows that have aired within the last 90 days. Unwatched shows are deleted after 90 days, ensuring efficient space management. Watched shows are retained on your server and can be organized into other automated Kometa collections, while the Series Premieres collection remains fresh and focused on the newest content. View a flow chart [Here](90DayPremieresflowchart.png)

### How It Works

This script is part of a larger workflow to manage and maintain TV show collections using various tools. Below is a breakdown of how it integrates:

1. **Trakt List (Series Premieres)**:
    - Manually add upcoming series premieres to a Trakt list.

2. **Kometa**:
    - Syncs with the Trakt list to create a Plex collection called "Series Premieres - 90 Day Trials."
    - Sends new items to Sonarr with the tag `trakt-premieres`.

    > **Kometa YAML**: An example configuration for Kometa is included in the repository. [View here](kometa-trakt-list-config.yaml).

3. **Sonarr**:
    - Downloads episodes and adds them to Plex, tagging them with `trakt-premieres`.

4. **Maintainerr**:
    - Monitors shows tagged with `trakt-premieres` and adds them to the "90-Day Rolling Delete" collection.
    - Automatically deletes unwatched shows older than 90 days.

    > **Maintainerr YAML**: An example configuration for Maintainerr is included in the repository. [View here](maintainerr_premieres_rule_.yaml).

5. **This Script**:
    - Runs daily to check the Trakt list.
    - Removes shows that have aired more than 90 days ago, based on data from TMDb.

6. **Kometa Collection**:
    - Always displays the freshest series premieres (aired within 90 days), whether watched or unwatched.

[Trakt.tv](https://trakt.tv) | [The Movie Database (TMDb)](https://www.themoviedb.org) | [Kometa](https://kometamp.com) | [Maintainerr](https://maintainerr.com)

