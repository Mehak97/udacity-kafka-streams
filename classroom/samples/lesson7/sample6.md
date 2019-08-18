## KSQL Aggregates

KSQL provides a number of useful aggregate functions, such as `MAX`/`MIN`, `SUM`, `COUNT` and
others.

In this exercise, we're going to see how we can create aggregated Tables from our KSQL queries.

### `SUM`

Let's first see how we can summarize purchases by currency.

```
SELECT currency, SUM(amount)
FROM purchases
GROUP BY currency;
```

When we run this query we will receive an output list that aggregates, by currency, the total value
of purchases by amount, to date, in that currency.

You will notice that values continue to print out to the screen on a periodic basis -- thats ok,
that just means the table-based representation is updating. You could instead create a table and
then periodically query that table to view updates.

### `HISTOGRAM`

Another useful function is `HISTOGRAM`, which allows us to count the number of occurrences for a
given value over a period of time. In this example, lets update the previous example with a
histogram, so not only will we have the `SUM` of all purchases, but also the number of times we've
had a purchase for that currency.

```
SELECT currency,
  SUM(amount) AS total_amount,
  HISTOGRAM(currency) AS num_purchases
FROM purchases
GROUP BY currency;
```

### `TOPK`

Another common usage of stream processing is to find the top number of some value in a window.

Let's define a tumbling time window of 30 seconds, and select the top 5 purchases by value, by
currency.

```
SELECT currency, TOPK(amount, 5)
FROM purchases
WINDOW TUMBLING (SIZE 30 SECONDS)
GROUP BY currency;
```

You'll see the window begin to scroll by. As the top 5 purchases by amount updates for each of our
currencies, the query will update. If you wait for 30 seconds, you will see the window reset.
