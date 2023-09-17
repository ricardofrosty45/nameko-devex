## Introduction
Hello guys! i hope you are doing well!
I'd like to provide some clarifications since the last feedback. T

he initial project encountered issues when running on my local environment. To address this, I made several changes, including upgrading software versions and modifying database schema creation due to errors encountered during table creation and database creation.

Now, let's dive into the comprehensive list of changes made from the project's inception, including updates that address previous feedback and introduce new enhancements.

## Changes Made

Here's a detailed list of the changes and updates made to the project:

- **Python Version**: The project has been updated to use Python 3.8 in the `environment_dev.yml` file. This update was necessary because Python 3.7 had been deprecated and couldn't run on my environment.

- **Pip Version**: Pip has been updated to version 22.0.1 to ensure compatibility with the project dependencies.

- **PostgreSQL Port**: The PostgreSQL port has been modified to a default value suitable for the project environment. This change was made because the default port was already in use on my machine.

- **Unit Tests**: All unit tests have been reviewed and updated to ensure they are working correctly. The test suite now provides accurate results, and issues have been fixed.

- **FastAPI Updates**: FastAPI endpoints have been updated with the correct RPC calls, and new RPC calls have been added. This ensures that the API interacts with the Nameko-based microservices as expected.

- **Performance and Smoke Tests**: Both performance tests and smoke tests have been verified and are functioning correctly, ensuring the API's robustness and reliability.

- **Clean-Up**: Temporary files that were cached have been cleaned up. The schema generator of Alembic has been configured to retain only the initial schema.

- **Database Schema**: The database schema has been modified to resolve issues that prevented the vanilla application from running. These changes necessitated the creation of a new Conda environment.

- **Linting**: The project now adheres to the default linting standards.

## Getting Started

To get started with this project, follow these steps:

1. Create a Conda environment with Python 3.8 running the command:

    ```bash
    $ conda env create -f environment_dev.yml
    ```

2. Activate the Conda environment:

    ```bash
    $ conda activate nameko-devex
    ```

3. Run Docker on your computer and then run this command:

    ```bash
    $ ./dev_run_backingsvcs.sh
    ```

4. There are two options for running the project:

    - Using FASTAPI, run this command:

        ```bash
        $ FASTAPI=X ./dev_run.sh orders.service products.service
        ```

    - Using the Gateway Service, run:

        ```bash
        $ ./dev_run.sh gateway.service orders.service products.service
        ```

5. After running this, you can run smoke tests, unit tests, or performance tests:

    - For smoke tests, run:

        ```bash
        $ ./test/nex-smoketest.sh local
        ```

    - For unit tests, execute:

        ```bash
        $ ./dev_pytest.sh
        ```

    - For performance tests, use:

        ```bash
        $ ./test/nex-bzt.sh local
        ```

## Appreciation
Thank you for your attention! I hope you have a nice day! 😄