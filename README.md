# Docs

Initializing the project- - pipenv install

Clery Logic

1. Creation of Boggy triggers signals to Berth model
   a) Berth objects created as per the Boggy fields of AC1, AC2 and so on.
2. Creation of ReservationChartForTrain for every Train based on their runs_on days (Monday to Sunday).
3. Deletion of Boggy and Berth objects for the previous day. (Can be 2 days or a week ago as well)
4. Deletion of ReservationChartForTrain objects for the previous day. (Can be 2 days or a week ago as well)

If Boggies are modified i.e, if (only) increased the number of coaches count, it will trigger the Berth increment via signals, and should be modified the new count of the total seats in the ReservationChartForTrain model as well.
