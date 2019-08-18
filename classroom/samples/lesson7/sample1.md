## Creating a Stream

In this demonstration you'll learn a few ways to create a KSQL Stream. Once you've created your
stream, you'll also see how to delete them.

Throughout this lesson we will refer to two topics:

* `com.udacity.streams.users`
* `com.udacity.streams.purchases`

`com.udacity.streams.users` has the following data shape:

**Key**: `<username: string>`
**Value**: ```
{
  "username": <string>,
  "email": <string>,
  "phone_number": <string>,
  "address": <string>
}
```

`com.udacity.streams.purchases` has the following data shape:

**Key**: `<username: string>`
**Value**: ```
{
  "username": <string>,
  "currency": <string>,
  "amount": <int>
}
```

### Showing Topics

The first step is to open the KSQL CLI.

```
root@c9827c86286f:/home/workspace# ksql

                  ===========================================
                  =        _  __ _____  ____  _             =
                  =       | |/ // ____|/ __ \| |            =
                  =       | ' /| (___ | |  | | |            =
                  =       |  <  \___ \| |  | | |            =
                  =       | . \ ____) | |__| | |____        =
                  =       |_|\_\_____/ \___\_\______|       =
                  =                                         =
                  =  Streaming SQL Engine for Apache Kafka® =
                  ===========================================

Copyright 2017-2018 Confluent Inc.

CLI v5.1.3, Server v5.1.3 located at http://localhost:8088

Having trouble? Type 'help' (case-insensitive) for a rundown of how things work!

ksql>
```

With the CLI Open, lets now see what Kafka Topics we have available to us:

```
ksql> SHOW TOPICS;

 Kafka Topic                   | Registered | Partitions | Partition Replicas | Consumers | ConsumerGroups
-----------------------------------------------------------------------------------------------------------
 _confluent-metrics            | false      | 12         | 1                  | 0         | 0
 _schemas                      | false      | 1          | 1                  | 0         | 0
 com.udacity.streams.purchases | false      | 1          | 1                  | 0         | 0
 com.udacity.streams.users     | false      | 1          | 1                  | 0         | 0
 connect-configs               | false      | 1          | 1                  | 0         | 0
 connect-offsets               | false      | 25         | 1                  | 0         | 0
 connect-status                | false      | 5          | 1                  | 0         | 0
-----------------------------------------------------------------------------------------------------------
```

you can see the two topics we're interested in -- `com.udacity.streams.purchases` and `com.udacity.streams.users`.

### Creating Streams

Next, we're going to create a stream for Purchases.

```
CREATE STREAM purchases
  (username VARCHAR,
   currency VARCHAR,
   amount INTEGER)
  WITH (KAFKA_TOPIC='com.udacity.streams.purchases',
        VALUE_FORMAT='JSON');
```

### Viewing available streams

We can see all available streams by running the `SHOW STREAMS` command

```
ksql> SHOW STREAMS;

 Stream Name | Kafka Topic                   | Format
------------------------------------------------------
 PURCHASES   | com.udacity.streams.purchases | JSON
------------------------------------------------------
```

### Create a Stream with a Query

KSQL Also allows for the creation of Streams derived from queries.

```
CREATE STREAM high_value_purchases AS
  SELECT * FROM purchases
  WHERE amount > 100000;
```

This would create a stream with purchases only valued above 100000

### Deleting a Stream

Finally, lets see how we can delete a stream.

```
DROP STREAM high_value_purchases;
```

You will immediately receive an error like the following:

```
ksql> DROP STREAM valuable_purchases;
Cannot drop VALUABLE_PURCHASES.
The following queries read from this source: [].
The following queries write into this source: [CSAS_VALUABLE_PURCHASES_0].
You need to terminate them before dropping VALUABLE_PURCHASES.
```

Under the covers KSQL is running a query to populate this stream. We first need to
terminate that query _before_ we can terminate the stream.

```
TERMINATE QUERY CSAS_VALUABLE_PURCHASES_0;
DROP STREAM valuable_purchases;
```

Now we have successfully terminated the underlying query and terminated the stream!

### Topic Management

In this demonstration, we created two streams -- `high_value_purchases` and `purchases`.

If we `SHOW TOPICS;` we'll notice a few interesting things:

```
ksql> SHOW TOPICS;

 Kafka Topic                   | Registered | Partitions | Partition Replicas | Consumers | ConsumerGroups
-----------------------------------------------------------------------------------------------------------
 _confluent-metrics            | false      | 12         | 1                  | 0         | 0
 _schemas                      | false      | 1          | 1                  | 0         | 0
 com.udacity.streams.purchases | true       | 10         | 1                  | 0         | 0
 com.udacity.streams.users     | false      | 10         | 1                  | 0         | 0
 connect-configs               | false      | 1          | 1                  | 0         | 0
 connect-offsets               | false      | 25         | 1                  | 0         | 0
 connect-status                | false      | 5          | 1                  | 0         | 0
 VALUABLE_PURCHASES            | false      | 4          | 1                  | 0         | 0
-----------------------------------------------------------------------------------------------------------
```

First, `VALUABLE_PURCHASES` topic has been created and is still present. By default, this is how
KSQL behaves. If you'd like to clean up the topic you need to do it manually. Second, why was a
`VALUABLE_PURCHASES` topic created, but not one for the stream `PURCHASES`? `VALUABLE_PURCHASES`
actually required modification to the data, so, an intermediate topic was created. `PURCHASES`,
however, required no modification, so the underlying topic is used as-is.
