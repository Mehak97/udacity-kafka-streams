### Hopping and Tumbling Windows

In this demonstration we'll see how to create Tables with windowing enabled.

### Tumbling Windows

Let's create a tumbling purchases table, where the window size is 30 seconds.

```
CREATE STREAM purchases_tumbling AS
  SELECT * FROM purchases
  WINDOW TUMBLING (SIZE 30 SECONDS);
```

### Hopping Windows

Now we can create a Table with a hopping window of 30 seconds with 5 second increments.

```
CREATE TABLE purchases_hopping AS
  SELECT username FROM purchases
  WINDOW HOPPING (SIZE 30 SECONDS, ADVANCE BY 5 SECONDS)
  WHERE username LIKE 'b%'
  GROUP BY username;
```

The above window is 30 seconds long and advances by 5 second. If you query the table you will see
the associated window times!

### Session Windows

Finally, lets see how session windows work. We're going to define the session as 5 minutes in
order to group many events to the same window

```
CREATE TABLE purchases_session AS
  SELECT username FROM purchases
  WINDOW SESSION (5 MINUTES)
  WHERE username LIKE 'b%'
  GROUP BY username;
```
