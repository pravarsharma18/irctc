# IRCTC Similar App

## Main Models:

- ### train APP

  - State
  - City
  - Station
  - Train
  - Boggy - Stores how many boggies can be attatch to a train on a Particular date.
  - Berth - Store the number of seats(L,M,U,SU,SL) in a Particular Boggy on a Particular date.

- ### reservation APP

  - PassengerDetail - Stores details of the passenger of the journey
  - Ticket - Stores the informations like PNR, passenger details, destination, source etc.
  - ReservationChartForTrain - Stores details of the passengerDetail, total seats, vacant_seats, waiting list if any for a particular date.

- ### users App

Initializing the project- - pipenv install

Clery Logic

1. Creation of Boggy triggers signals to Berth model
   a) Berth objects created as per the Boggy fields of AC1, AC2 and so on.
2. Creation of ReservationChartForTrain for every Train based on their runs_on days (Monday to Sunday).
3. Deletion of Boggy and Berth objects for the previous day. (Can be 2 days or a week ago as well)
4. Deletion of ReservationChartForTrain objects for the previous day. (Can be 2 days or a week ago as well)

If Boggies are modified i.e, if (only) increased the number of coaches count, it will trigger the Berth increment via signals, and should be modified the new count of the total seats in the ReservationChartForTrain model as well.
