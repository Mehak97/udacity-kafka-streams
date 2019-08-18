### Querying in KSQL

Ad-hoc querying in KSQL is one of the tools greatest strengths. Lets have a look at some sample
queries.

### Basic filtering

We've already seen how to filter data in the table creation process, but lets revisit it one more
time

```
SELECT username, amount
  FROM purchases
  WHERE amount > 100000
    AND username LIKE 'k%';
```

### Scalar Functions

KSQL Provides a number of [Scalar functions for us to make use of](https://docs.confluent.io/current/ksql/docs/developer-guide/syntax-reference.html#scalar-functions).

Lets write a function that takes advantage of some of these features:

```
SELECT CONCAT(CONCAT(CONCAT(CONCAT(UCASE(username), ', '), currency), ', '), CAST(FLOOR(amount/100.0) AS VARCHAR))
  FROM purchases
  WHERE amount > 100000
    AND username LIKE 'k%';
```

This query will produce a single CSV-like Output where the username is capitalized and the amount
is divided by 100 and rounded to the ceiling.

The `CONCAT` function takes _two_ strings and joins them together.
The `UCASE` function takes a string and capitalizes it.
The `CAST` function takes a variable in one format and transforms it into another.

### Terminating Queries

**`SELECT` queries are not persistent!**

Notice that as soon as you hit `CTRL+C` your query ends. When you run the query again, KSQL has to
recreate the query. This means that if you want the results of this query to be persistent, you
need to create a Table or a Stream.
