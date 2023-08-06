# mcap2timescale

mcap2timescale transforms `.mcap` and `.bag` (ROS bag) files into a Timescale database. You can now query any robotics data using SQL without writing ETLs.

## Hosted solution

We will soon offer a hosted solution with a number of perks:
* Managed ingestion, database, and infrastructure for integrations (e.g. S3, Grafana).
* Reverse Timescale to `.mcap` and `.bag` generator.
* Vector search for imagery, audio, and other unstructured data.
* Web interface to track and share data with your team.

## Running yourself

1. Set up a Timescale database. Take note of all connection details (host, port, username, password, and database name).

2. Install this package.
```
pip install mcap2timescale
```

3. Run the job against any file. The database connection arguments are optional.
```
mcap2timescale /path/to/file.mcap \
    --host localhost \
    --port 5432 \
    --user postgres \
    --password password \
    --name postgres
```

4. Connect to your database and run any query.

## Design considerations

* __Timescale Hypertables__: this project creates hypertables with Timescale. Due to the sheer quantity of messages, it is critical make use of Timescale's compression features.
* __No ROS Dependency:__ this project runs without any ROS dependencies. It is a pain to install ROS simply to extract data from ROS bag or MCAP files. We leverage the `rosbags` project to accomplish this by dynamically loading message schemas at runtime.
* __Transform MCAP to ROS bag__: this project converts all MCAP files into ROS bags before transforming the data to avoid needing to rewrite the ingestion flow.
