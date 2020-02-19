# Weather Based Engagement

This is a simple command line module which gives recommendations for customer engagement methods based on the weather over the next five days.

The weather data is retrieved from the API provided by openweathermap.org.

The rules for determining the best method of engagement are as follows:

1. The best time to engage a customer via a text message is when it is sunny and warmer than 75 degrees Fahrenheit.
2. The best time to engage a customer via email is when it is between 55 and 75 degrees Fahrenheit.
3. The best time to engage a customer via a phone call is when it is less than 55 degrees or when it is raining.

## Running

1. Create a virtual environment
    
        python3 -m venv venv
        source venv/bin/activate
        
2. Run the command line tool
        
        python3 -m app
        
## Testing

After following the above steps to create the virtual environment
    
        python3 -m pytest
