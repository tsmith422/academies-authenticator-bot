# Academies Authenticator Bot | ``Rev Bot``
A bot programmed using python in order to authenticate engineering academy org members to give them access to the full discord.<br><br>

<div align="center">
  <img src="https://github.com/tsmith422/academies-authenticator-bot/assets/143378368/93bbd1e9-00cd-43e4-bfcf-96b6dcbf7129" width="200" height="200"><br>
  <figcaption><em>Profile picture for <code>Rev Bot</code> drawn by TEASO's Maceo Baez</em></figcaption>
</div>

## Overview
This is a project that the **Texas Engineering Academies Student Organization (TEASO)** tasked me with doing after I became an officer of the org.

While I had a decent amount of python knowledge, I had never created a discord bot before (or worked with an API in general for that matter), so I knew this would be an excellent opportunity to learn and apply my coding knowledge to an actual issue the organization was running into.

### What TEASO needed help with
- The organization has a one-time payment in order for students to gain access to all the important channels in the discord.
- Members who pay the fee gain the role **Verified**, this is what allows them to gain access to all the resources the org provides.
- The bot aims to automatically change roles of members who pay the fee so that officers do not have to continue manually assigning roles.

## How the bot works
The bot solves this issue by utilizing the Google spreadsheets API:
- Members fill out a form in order to conclude their admission in the organization.
- Information from that form is saved on a spreadsheet.
- The bot utilizes Google’s spreadsheet API to read through and confirm a user has gotten their information onto the spreadsheet, if the information matches then the user is verified.

This method works great because the API allows for real-time updates on the spreadsheet so anyone who fills out the form can immediately confirm their verification in the discord.

## The future of the bot
While this bot is primarily used for authentication of new organization members, I plan for it to do other tasks that the org’s discord could benefit from. These changes will be documented as I do them.

I wanted to make the code as understandable as I could for future organization officers to be able to update the bot if any changes are needed.

*Copyright (c) 2024 Taylor Smith*
