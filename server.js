const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const path = require('path');
const { exec } = require('child_process');
const { PythonShell } = require('python-shell');



const app = express();

// set up ejs view engine 
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'ejs');

app.use(cors())
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(express.static(__dirname + '../public'));

/* GET home page, respond by rendering index.ejs */
app.get('', async (req, res) => {
    const { stockName, period, interval, openPrice, low, high, volume } = req.query;
    console.log(stockName);
    console.log(period);
    console.log(interval);
    console.log(openPrice);
    console.log(low);
    console.log(high);
    console.log(volume);
    let options = {
        pythonPath: '/Users/aryanmalhotra/opt/anaconda3/bin/',
        args: ['activate', 'base', './project/project.py', 'GOOG', '5y', '1d', '50', '49', '51', '54000000']
      };
      
      PythonShell.run('conda', options, function (err, results) {
        if (err) throw err;
        console.log('results:', results);
        res.json(results)
      });
    // const result = await callRegression(stockName, period, interval, openPrice, low, high, volume);
    // res.send(result);
    
});
function callRegression(stockName, period, interval, openPrice, low, high, volume) {
    return new Promise((resolve, reject) => {
      exec(`python -c "from ./project/project.py import get_predicted_price('${stockName}', '${period}', '${interval}', '${openPrice}', '${low}', '${high}', '${volume}')"`, (error, stdout, stderr) => {
        if (error) {
          console.error(`exec error: ${error}`);
          reject(error);
        }
        console.log(`stdout: ${stdout}`);
        console.error(`stderr: ${stderr}`);
        resolve(stdout);
      });
    });
  }
  
app.listen("4242", function () {
    console.log(`Node app is running on port 4242`);
});