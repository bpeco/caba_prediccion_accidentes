
# Accident Prediction Model in Buenos Aires

In this repository you will find the Final Project of Group #7 in relation to the Data Science course | Digital House.

The jupyter notebook's name is: "TRABAJO FINAL INTEGRADOR - GRUPO 7.ipynb"
<hr>
Note: the notebooks are commented in Spanish. I am currently working on translating them.
<hr>
In the meantime, I leave some general comments on:
<ul>
  <li> 💡 What motivated this project?</li>
  <li> 🦶🏼 What were the steps we followed?</li>
  <li> 🛫 How we deployed our model?</li>
  <li> ⏭️ Next steps?</li>
</ul>


`💡 What motivated this project?`

Today an ambulance from the Emergency Medical Care System takes approximately 20 to 30 minutes to reach the scene of an accident (<a href = "https://www.lanacion.com.ar/sociedad/same-una- emergency-every-155-minutes-nid1442582 / "> Reference </a>). This time of arrival is in the best of cases when the call is made to 107 and not to 911, as it happens many times and in the transfer of the urgency even more time is lost. Lost minutes that could be very valuable ...

The idea of this project is to be able to predict the number of accidents that may occur in a certain area of the Autonomous City of Buenos Aires, considering different variables of dates and weather conditions. Therefore, Ambulatory Spots could be located in areas of greater risk of traffic accidents, reaching these places more quickly.

In order to achieve this, a dataset that was obtained from the <a href="https://data.buenosaires.gob.ar/dataset/"> CABA </a> page was developed, along with other data obtained through a scrapping performed on the page <a href="https://www.wunderground.com/"> Wunderground </a>.

`🦶🏼 What were the steps we followed?`

<ul>
  <li> ✅    Data cleaning</li>
  <li> ✅    WebScrapping for the weather data</li>
  <li> ✅    EDA </li>
  <li> ✅    2-step-stage to train our models </li>
</ul>

`🛫 How we deployed our model?`

We developed a page where you could choose the time of day, the state of the weather and the neighborhood from which you wanted to know the number of accidents that could happen.

`⏭️ Next steps?`

There are many variables that, due to time and resources, we decided not to investigate and include them in the project. For example, the maximum speeds in each neighborhood, the number of unsignalized crossings, etc. These types of variables and others, it would be interesting to analyze their relationship with the possible occurrence or not of an accident.
Moreover, a possible variation on this project could be trying to predict accidents in a smaller geographic unit than neighborhoods.
