# Timeclock

## Development Environment

- [Pipenv](https://pipenv.pypa.io/en/latest/)
- Python 3.9+

## How to install locally

### 1. Install pipenv and use pipenv to create development environemnt

```
pipenv shell
pipenv install
```

### 2. Create database
```
python manage.py migrate
```

## How to test


### 1. Add testing data

```
python manage.py shell < test.py
```

### 2. Download Insomnia

https://insomnia.rest/download

### 3. Import data to Insomnia

data is in `docs/Insomnia_2022-05-21.json`

[Import and Export Data](https://docs.insomnia.rest/insomnia/import-export-data)

### 4. Create User by using Insomnia

You could create new user by using `createUser` request,

or get token by using default test user in `obtainToken` request.

### 5. Get token

Token could be got from `obtainToken` request.

After get new token, put in in `Header`.

Field name - `AUTHORIZATION`

Field value - `JWT {this is your token}`


## GraphQL Schema

```GraphQL
schema {
	query: Query
	mutation: Mutation 
}

type CreateUser { 
	user: UserType
}

type ClockIn {
  clock: ClockType
}

type ClockOut {
  clock: ClockType
}

type CurrentClock { 
	clock: ClockType
}

type ClockedHours {
	today: Int 
	currentWeek: Int 
	currentMonth: Int
}

type ClockType {
	id: ID!
	user: UserType! 
	clockedIn: DateTime! 
	clockedOut: DateTime
}

type UserType {
	id: ID!
	username: String! 
	email: String!
}

scalar GenericScalar
scalar DateTime

type ObtainJSONWebToken { 
	payload: GenericScalar! 
	refreshExpiresIn: Int!
	token: String!
}

type Mutation {
	clockIn: ClockIn
	clockOut: ClockOut
	createUser(email: String!, password: String!, username: String!): CreateUser 
	obtainToken(username: String!, password: String!): ObtainJSONWebToken

}

type Query {
	me: UserType
	currentClock: CurrentClock 
	clockedHours: ClockedHours 
}
```