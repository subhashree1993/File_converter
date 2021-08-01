## File Coverter Application using 3rd Party API

### Features:
- User Registration
- User Login
- File Upload and Convertion using (https://cloudconvert.com)
- Show Previous Conversion Logs


### DB Design:
Design of User Table

```sql
'id'(pk), 'name', 'email'(unique), 'password'
```

Design of File converter Table

```sql
'id'(pk), 'userId','fileName', 'originalFilePath', 'convertedFilePath','convertedFrom', 'convertedTo', 'requestedTime', 'conversionStatus'
```


### 3rd Party Api (https://cloudconvert.com/api/v2#overview)
> **Limitations**: 
> 25 Free API hits per day, after that payment has to be done to do conversion of file formats

