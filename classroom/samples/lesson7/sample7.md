### KSQL JOINs

KSQL also supports `JOIN` operations. In this demonstration you will see how to join the purchases
stream to the users table.

Before we move on, its worth remember that we __cannot__ `JOIN` a Table to a Stream, me way
**only** join a Stream to a Table.

### `LEFT OUTER JOIN`

In KSQL, as with most SQL derivatives, the default `JOIN` is the `LEFT OUTER JOIN`.

Let's perform a `LEFT OUTER JOIN`, or simply, `JOIN` on Purchases to Users.

```
CREATE TABLE user_purchases AS
  SELECT u.username, u.address, u.phone_number, u.email, p.amount, p.currency
  FROM purchases p
  JOIN users u on u.username = p.username;
```

### `INNER JOIN`

KSQL also supports `INNER JOIN` between Streams and Tables

```
CREATE TABLE user_purchases AS
  SELECT u.username, u.address, u.phone_number, u.email, p.amount, p.currency
  FROM purchases p
  INNER JOIN users u on u.username = p.username;
```

### `FULL OUTER JOIN`

Alright, lets wrap up by trying KSQLs final supported JOIN operation, the `FULL OUTER JOIN`

```
CREATE TABLE user_purchases AS
  SELECT u.username, u.address, u.phone_number, u.email, p.amount, p.currency
  FROM purchases p
  FULL OUTER JOIN users u on u.username = p.username;
```

The query will fail to run:

`> Full outer joins between streams and tables (stream: left, table: right) are not supported.`

KSQL only supports `FULL OUTER JOIN` when joining a _Table to a Table_ or a _Stream to a Stream`.
