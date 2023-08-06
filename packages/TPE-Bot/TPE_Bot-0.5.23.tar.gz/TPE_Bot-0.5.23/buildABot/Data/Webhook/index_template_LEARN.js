// See https://github.com/dialogflow/dialogflow-fulfillment-nodejs
// for Dialogflow fulfillment library docs, samples, and to report issues
'use strict';
 
const functions = require('firebase-functions');
const {WebhookClient} = require('dialogflow-fulfillment');
const {Card, Payload, Suggestion} = require('dialogflow-fulfillment');
const crypto = require('crypto');

// Node Mailer Declaration
const nodemailer = require('nodemailer');
const transporter = nodemailer.createTransport({
  service: 'gmail',
      auth: {
        user: 'tpbot.main@gmail.com',
        pass: 'xxhdwtuzeecdjmtm'
      }
});

//Firebase Declaration
const admin = require('firebase-admin');
const serviceAccount = SERVICEACCOUNTKEYHERE; //GET SERVICE ACCOUNT KEY FROM GCP
admin.initializeApp({
  credential: admin.credential.cert(serviceAccount),
  databaseURL: "DBURLHERE" //FIREBASE DB URL
});

process.env.DEBUG = 'dialogflow:debug';
 
exports.dialogflowFirebaseFulfillment = functions.https.onRequest((request, response) => {
  const agent = new WebhookClient({ request, response });
  console.log('Dialogflow Request headers: ' + JSON.stringify(request.headers));
  console.log('Dialogflow Request body: ' + JSON.stringify(request.body));
 
  function sendStudentEnquiry(agent){
    const email = agent.parameters.email;
    const name = agent.parameters.name;
    const message = agent.parameters.message;
    
    const mailOptions = {
      from: 'tpbot.main@gmail.com',
      to: 'TUTOREMAILHERE@tp.edu.sg', //TUTOR'S EMAIL
      subject: "Student's Enquiry from Chatbot",
      text: "Hi, \n\n A student has questions on the subject. Please review." + 
      '\n\n Student: ' + name + '\n\n Email: ' + email + '\n\n Enquiry: ' + message + 
      '\n\n Best Regards, \n Dialogflow Chatbot'
    };
    
    transporter.sendMail(mailOptions, function(error, info){
      if (error) {
        agent.add("Error while sending");
        console.log(error);
      } 
      
      else {
        agent.add("Email sent!");
        console.log('Email sent: ' + info.response);
      }
    });
  }
  
  function loginGreeting(agent)
  {
    const hash = crypto.createHash('sha224');
    const string = agent.parameters.loginID;
    const hashedString = hash.update(string, 'utf-8');
    const gen_hash = hashedString.digest('hex');

    var id;
    var ref = admin.database().ref("ID");
    ref.orderByValue().equalTo(gen_hash).on("child_added", function(snapshot){
      id = snapshot.key;
    });

    return admin.database().ref().once("value").then(function(snapshot) {
      var name = snapshot.child("/NAME/"+id).val();
      agent.add("Login Successful! 💁🏻‍♀️");
      agent.add("Hi "+ name + ", how do you feel today? 🧐");
      const payload = {
                        "richContent": [
                          [
                            {
                              "type": "chips",
                              "options": [
                                {
                                  "text": "Awesome 😄"
                                },
                                {
                                  "text": "Doing fine 🙂"
                                },
                                {
                                  "text": "Still hanging there 😐"
                                },
                                {
                                  "text": "It's been a rough week 😔"
                                }
                              ]
                            }
                          ]
                        ]
                      };
      const payloadTele = {

        "telegram": {

          "text": "Select a mood:",

          "reply_markup": {

            "keyboard": [

              [

                {

                  "callback_data": "Awesome 😄",

                  "text": "Awesome 😄"

                }

              ],

              [

                {

                  "callback_data": "Doing fine 🙂",

                  "text": "Doing fine 🙂"

                }

              ],

              [

                {

                  "callback_data": "Still hanging there 😐",

                  "text": "Still hanging there 😐"

                }

              ],

              [

                {

                  "callback_data": "It's been a rough week 😔",

                  "text": "It's been a rough week 😔"

                }

              ]

            ]

          }

        }

      };
      agent.add(new Payload(agent.UNSPECIFIED, payload, { rawPayload: true, sendAsMessage: true }));
      agent.add(new Payload(agent.TELEGRAM, payloadTele, {rawPayload: true, sendAsMessage: true}));

    });
  }

  function remembername(agent)
  {
    const hash = crypto.createHash('sha224');
    const string = agent.parameters.loginID;
    const hashedString = hash.update(string, 'utf-8');
    const gen_hash = hashedString.digest('hex');

    var id;
    var ref = admin.database().ref("ID");
    ref.orderByValue().equalTo(gen_hash).on("child_added", function(snapshot){
      id = snapshot.key;
    });

    return admin.database().ref().once("value").then(function(snapshot) {
      var name = snapshot.child("/NAME/"+id).val();
      agent.add("Hi "+ name + ", welcome back!");
      const payload = {
                        "richContent": [
                          [
                            {
                              "type": "chips",
                              "options": [
                                {
                                  "text": "Learn & Explore"
                                },
                                {
                                  "text": "Results & Recommendation"
                                }
                              ]
                            }
                          ]
                        ]
                      };
      const payloadTele = {

        "telegram": {

          "text": "Select a menu:",

          "reply_markup": {

              "keyboard": [

              [

                  {

                  "text": "🔎 Learn & Explore",

                  "callback_data": "Learn & Explore"

                  }

              ],

              [

                  {

                  "text": "🖋 Results & Recommendation",

                  "callback_data": "Results & Recommendation"

                  }

              ]

              ]

          }

        }

      };
      agent.add(new Payload(agent.UNSPECIFIED, payload, { rawPayload: true, sendAsMessage: true }));
      agent.add(new Payload(agent.TELEGRAM, payloadTele, { rawPayload: true, sendAsMessage: true }));

    });
  }


  // Run the proper function handler based on the matched Dialogflow intent name
  let intentMap = new Map();
  intentMap.set('Email Enquiry', sendStudentEnquiry);
  intentMap.set('Log In', loginGreeting);
  intentMap.set('Log In - Remember Name', remembername);
  agent.handleRequest(intentMap);
});
