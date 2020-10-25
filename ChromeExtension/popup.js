// Copyright 2018 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

'use strict';

let changeColor = document.getElementById('changeColor');

chrome.storage.sync.get('color', function(data) {
  changeColor.style.backgroundColor = data.color;
  changeColor.setAttribute('value', data.color);
});

changeColor.onclick = function(element) {
  let color = element.target.value;
  chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
    console.log(tabs)
    chrome.tabs.executeScript(
        tabs[0].id,
        {code: 'document.body.style.backgroundColor = "' + color + '";'});
  });
};

document.getElementById("test").addEventListener('click', () => {
  console.log("Popup DOM fully loaded and parsed");
  function modifyDOM() {
      //You can play with your DOM here or check URL against your regex
      console.log('Tab script:');
      console.log(document.body);
      //We get the coordinate of the DOM objects
      let all = document.getElementsByTagName("*");
      let Objloc = []
      for (var i=0, max=all.length; i < max; i++) {
        // Do something with the element here
        let element = all[i].getBoundingClientRect();
        Objloc.push([element.top, element.right, element.bottom, element.left])
        //console.log(element.top, element.right, element.bottom, element.left);
      }
      
      
      //Attempt to communicate to background.js
      chrome.runtime.sendMessage({greeting: "hello", objectLocations: Objloc }, function(response) {
        //console.log(response.farewell);
      });
      return Objloc;
  }
  
  //We have permission to access the activeTab, so we can call chrome.tabs.executeScript:
  chrome.tabs.executeScript({
      code: '(' + modifyDOM + ')();' //argument here is a string but function.toString() returns function's code
  }, (results) => {
      //Here we have just the innerHTML and not DOM structure
      //talk to local websocket server
      WebSocketCall(results[0].map((element)=>{return element.join("|")}))
      console.log('Popup script:')
      console.log(results[0]);
  });
});