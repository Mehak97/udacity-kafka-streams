# Kafka CLI Tools

In this exercise, you will learn how to use the most common Kafka CLI tools.

## Listing topics

First, lets see how to list topics that already exist within Kafka.

`kafka-topics --list --zookeeper localhost:2181`

When you run this command, you should see output like the following:

```
__confluent.support.metrics
__consumer_offsets
_confluent-ksql-ksql_service_docker_command_topic
_schemas
connect-config
connect-offset
connect-status
```

The `--list` switch tells the `kafka-topics` CLI to list all known topics.

The `--zookeeper localhost:2181` switch tells the `kafka-topics` CLI where the
Zookeeper ensemble Kafka is using is located. Note that in the newest versions of Kafka the
`--zookeeper` switch is deprecated in favor of a `--bootstrap-server` switch that points to Kafka. The `--zookeeper` switch still works, but will likely be dropped in the next major revision of Kafka.

We haven't created any topics yet, so what you're seeing are system topics that Kafka and other
Kafka ecosystem tools make use of.

## Creating topics

Now that we've seen what topics exist, let's create one.

`kafka-topics --create --topic "my-first-topic" --partitions 1 --replication-factor 1 --zookeeper localhost:2181`

When you run this command it should silently exit after a few moments.

The switch `--topic "my-first-topic"` tells Kafka what to name the topic

The switch `--partitions 1` and the switch `--replication-factor 1` are required configuration
which we will explore more in the next lesson.

To check that our topic was successfully created, lets repeat the command to list topics with a
slight modification:

`kafka-topics --list --zookeeper localhost:2181 --topic "my-first-topic"`

Now, a single topic should be printed, like so:

```
my-first-topic
```

## Producing data

Now that we have a topic, lets add some data.

`kafka-console-producer --topic "my-first-topic" --broker-list PLAINTEXT://localhost:9092`

The switch `--broker-list` serves the same purpose as `--boostrap-server` for the `kafka-topics`
command -- it simply tells the tool where to find Kafka.

When you hit enter, you should be dropped into an interactive terminal.

Try typing out a few messages and hitting enter.

```
root@6b48dc2bd81c:/# kafka-console-producer --topic "my-first-topic" --broker-list PLAINTEXT://localhost:9092
>hello
>world!
>my
>first
>kafka
>events!
>
```

## Consuming data

While its great that we've produced data, it would be more exciting if we could see it being
consumed.

Open a new terminal tab and run the following command:

`kafka-console-consumer --topic "my-first-topic" --bootstrap-server PLAINTEXT://localhost:9092`

Notice that nothing prints out? Remember that by default Kafka doesnt provide historical messages
to new consumers. Return to the producer and enter a few new messages. You should see them come
across the screen!

Hit `Ctrl+C` to exit the consumer. Lets try this again, but ask Kafka to provide all the messages
that have been published to the topic:

`kafka-console-consumer --topic "my-first-topic" --bootstrap-server PLAINTEXT://localhost:9092 --from-beginning`

The `--from-beginning` switch tells `kafka-console-consumer` to read data from the beginning of the
topic, not just data from when we connect.

You should now see output that includes all of the messages you've produced:

```
root@6b48dc2bd81c:/# kafka-console-consumer --topic "my-first-topic" --bootstrap-server PLAINTEXT://localhost:9092 --from-beginning
hello
world!
my
first
kafka
events!
hello again!
```

## Deleting topics

Now that we've explored working with the CLI tools, lets clean up our topic.

`kafka-topics --delete --topic "my-first-topic" --bootstrap-server PLAINTEXT://localhost:9092`

This command is identical to the `--create` command from earlier, except now we're calling the
command with the `--delete` switch instead.

This command does not print any output if its successful. To check that your topic is actually
delete, list the topics one more time:

`kafka-topics --list --zookeeper localhost:2181`

`my-first-topic` should no longer appear in the list of topics.

