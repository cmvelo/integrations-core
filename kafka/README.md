# Agent Check: Kafka

![Kafka Dashboard][30]

## Overview

Connect Kafka to Datadog to:

* Visualize the performance of your cluster in real time.
* Correlate the performance of Kafka with the rest of your applications.

This check has a limit of 350 metrics per instance. The number of returned metrics is indicated on the info page. Specify the metrics you are interested in by editing the configuration below. To learn how to customize the metrics to collect visit the [JMX Checks documentation][13] for more detailed instructions.

To collect Kafka consumer metrics, see the [kafka_consumer check][14].

## Setup
### Installation

The Agent's Kafka check is included in the [Datadog Agent][15] package, so you don't need to install anything else on your Kafka nodes.

The check collects metrics via JMX, so you need a JVM on each kafka node so the Agent can fork [jmxfetch][16]. You can use the same JVM that Kafka uses.

### Configuration

Edit the `kafka.d/conf.yaml` file,  in the `conf.d/` folder at the root of your [Agent's configuration directory][31].

#### Metric Collection

**The following instructions are for the Datadog agent >= 5.0. For agents before that, see the [older documentation][17].**

Kafka bean names depend on the exact Kafka version you're running. Use the [example configuration file][18] that comes packaged with the Agent as a base since it is the most up-to-date configuration. **Note**: the Agent version in the example may be for a newer version of the Agent than what you have installed.

After you've configured `kafka.yaml`, [restart the Agent][19] to begin sending Kafka metrics to Datadog.

#### Log Collection

**Available for Agent >6.0**

Kafka uses the `log4j` logger by default. To activate logging to a file and customize the format edit the `log4j.properties` file:

```
# Set root logger level to INFO and its only appender to R
log4j.rootLogger=INFO, R
log4j.appender.R.File=/var/log/kafka/server.log
log4j.appender.R.layout=org.apache.log4j.PatternLayout
log4j.appender.R.layout.ConversionPattern=%d{yyyy-MM-dd HH:mm:ss} %-5p %c{1}:%L - %m%n
```

By default, our integration pipeline supports the following conversion patterns:

  ```
  %d{yyyy-MM-dd HH:mm:ss} %-5p %c{1}:%L - %m%n
  %d [%t] %-5p %c - %m%n
  %r [%t] %p %c %x - %m%n
  ```

Clone and edit the [integration pipeline][20] if you have a different format.

* Collecting logs is disabled by default in the Datadog Agent, enable it in your `datadog.yaml` file with:

  ```
  logs_enabled: true
  ```

* Add the following configuration block to your `kafka.d/conf.yaml` file. Change the `path` and `service` parameter values based on your environment. See the [sample kafka.d/conf.yaml][18] for all available configuration options.

  ```
  logs:
    - type: file
      path: /var/log/kafka/server.log
      source: kafka
      service: myapp
      #To handle multi line that starts with yyyy-mm-dd use the following pattern
      #log_processing_rules:
      #  - type: multi_line
      #    name: log_start_with_date
      #    pattern: \d{4}\-(0?[1-9]|1[012])\-(0?[1-9]|[12][0-9]|3[01])
  ```

* [Restart the Agent][19].

**Learn more about log collection [in the log documentation][21]**

### Validation

[Run the Agent's status subcommand][22] and look for `kafka` under the **JMXFetch** section:

```
========
JMXFetch
========
  Initialized checks
  ==================
    kafka
      instance_name : kafka-localhost-9999
      message : 
      metric_count : 46
      service_check_count : 0
      status : OK
```

## Data Collected
### Metrics
See [metadata.csv][23] for a list of metrics provided by this check.

### Events
The Kafka check does not include any events at this time.

### Service Checks
**kafka.can_connect**  
Returns `CRITICAL` if the Agent is unable to connect to and collect metrics from the monitored Kafka instance, otherwise returns `OK`.

## Troubleshooting

* [Troubleshooting and Deep Dive for Kafka][24]
* [Agent failed to retrieve RMIServer stub][25]
* [Producer and Consumer metrics don't appear in my Datadog application][26]

## Further Reading

* [Monitoring Kafka performance metrics][27]
* [Collecting Kafka performance metrics][28]
* [Monitoring Kafka with Datadog][29]


[13]: https://docs.datadoghq.com/integrations/java/
[14]: https://docs.datadoghq.com/integrations/kafka/#agent-check-kafka-consumer
[15]: https://app.datadoghq.com/account/settings#agent
[16]: https://github.com/DataDog/jmxfetch
[17]: https://github.com/DataDog/dd-agent/wiki/Deprecated-instructions-to-install-python-dependencies-for-the-Datadog-Agent
[18]: https://github.com/DataDog/integrations-core/blob/master/kafka/datadog_checks/kafka/data/conf.yaml.example
[19]: https://docs.datadoghq.com/agent/faq/agent-commands/#start-stop-restart-the-agent
[20]: https://docs.datadoghq.com/logs/processing/#integration-pipelines
[21]: https://docs.datadoghq.com/logs
[22]: https://docs.datadoghq.com/agent/faq/agent-commands/#agent-status-and-information
[23]: https://github.com/DataDog/integrations-core/blob/master/kafka/metadata.csv
[24]: https://docs.datadoghq.com/integrations/faq/troubleshooting-and-deep-dive-for-kafka
[25]: https://docs.datadoghq.com/integrations/faq/agent-failed-to-retrieve-rmierver-stub
[26]: https://docs.datadoghq.com/integrations/faq/producer-and-consumer-metrics-don-t-appear-in-my-datadog-application
[27]: https://www.datadoghq.com/blog/monitoring-kafka-performance-metrics/
[28]: https://www.datadoghq.com/blog/collecting-kafka-performance-metrics/
[29]: https://www.datadoghq.com/blog/monitor-kafka-with-datadog/
[30]: https://raw.githubusercontent.com/DataDog/integrations-core/master/kafka/images/kafka_dashboard.png
[31]: https://docs.datadoghq.com/agent/faq/agent-configuration-files/#agent-configuration-directory
