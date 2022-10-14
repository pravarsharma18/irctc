# Train Booking App

## Project Setup

- Installing Dependencies
  ```
  pipenv install
  ```
  ```
  python manage.py migrate
  ```
  ```
  python manage.py createsuperuser
  ```
- Celery beat command
  ```
  celery -A irctc worker -l info --beat
  ```

## Main Models:

- ### train APP

  - State
  - City
  - Station
  - Train
  - Boggy - Stores how many boggies can be attatch to a train on a Particular date.
  - Berth - Store the number of seats(L,M,U,SU,SL) in a Particular Boggy on a Particular date.

  #### Logic

  - Train model has Station as many to many field, which is managed by "through" model TrainWithStations, having sequence, distance, base fare, arrival time, departure time, This will be helpful for the ordering the train vai source and destination and vice versa.
  - Train model's queryset manager also has 'singles' method to get the single train distinct vai number.
  - Train model's queryset manager also has 'get_total_seats' method which calculates the sum of all the seats in a particular train given on a particular date.

- ### reservation APP

  - PassengerDetail - Stores details of the passenger of the journey
  - Ticket - Stores the informations like PNR, passenger details, destination, source etc.
  - ReservationChartForTrain - Stores details of the passengerDetail, total seats, vacant_seats, waiting list if any for a particular date.

- ### users App

  - User - Inhertited from AbstractUser class, Users can login via username, mobile number as well as email.

- ### base App
  Contains all the constants used in the project in choices.py file.

## Celery Logic

1. Creation of Boggy triggers signals to Berth model.
   a) Berth objects created as per the Boggy fields of AC1, AC2 and so on.
2. Creation of ReservationChartForTrain for every Train based on their runs_on days (Monday to Sunday).
3. Deletion of Boggy and Berth objects for the previous day. (Can be 2 days or a week ago as well).
4. Deletion of ReservationChartForTrain objects for the previous day. (Can be 2 days or a week ago as well).

If Boggies are modified i.e, if (only) increased the number of coaches count, it will trigger the Berth increment via signals, and should be modified the new count of the total seats in the ReservationChartForTrain model as well.

## Logic

1. BOOKING_FOR_NEXT_DAYS flag responsible for booking a train, right now it is set to 10 days.
2. Filtering train by source, destination and date.
