<p align="center">
  <img width="125" height="186" src="https://github.com/Ziconius/Fudge/blob/master/FudgeC2/ServerApp/static/images/fudge.png">
</p>


# FudgeC2
[![Commit Activity](https://img.shields.io/github/commit-activity/m/ziconius/fudgec2)](https://github.com/ziconius/FudgeC2/graphs/commit-activity)
[![Code Quality](https://img.shields.io/codeclimate/maintainability-percentage/Ziconius/FudgeC2)](https://codeclimate.com/github/Ziconius/FudgeC2)
[![Licence](https://img.shields.io/github/license/ziconius/fudgec2)](https://github.com/ziconius/FudgeC2/blob/master/LICENSE.txt)
[![Stars](https://img.shields.io/github/stars/ziconius/fudgec2)](https://github.com/Ziconius/FudgeC2/stargazers)


FudgeC2 is a Powershell command and control platform designed to facilitate team collaboration and campaign timelining, which aims to help clients better understand red team activities.

Built on Python3 with a web frontend, FudgeC2 aims to provide red teamers a simple interface in which to manage active implants across their campaigns.

_FudgeC2 is currently in beta, and should be used with caution in non-test environments. The beta was release at BlackHat Arsenal USA 2019._

Table of Contents:
< HERE >

### Installation

To install & run FudgeC2  run the following:

```
git clone https://github.com/Ziconius/FudgeC2
cd FudgeC2/FudgeC2
sudo pip3 install -r requirements.txt
sudo python3 Controller.py
```
You will then be able to access the platform from 127.0.0.1:5001/. The first-time logon credentials are:

`admin`:`letmein`

For those who wish to use FudgeC2 via Docker, you can find the Docker [here](/Dockerfile).

For more information on installation and configuration see the wiki, [here](https://github.com/Ziconius/FudgeC2/wiki).

### Usage

FudgeC2 breaks projects down into campaigns. Each campaign will have a their own implant templates, active implants, users, and targets.

Once you have generated a campaign and implant you will be able to interact with the any active implants from the campaign homepage. The

<Homepage screenshot>

An overview of functionality can be seen below, for more information see the implant functionality pages on FudgeC2s' wiki, [found here](https://github.com/Ziconius/FudgeC2/wiki).

Builtin functionality
- ```<command>``` If no builtin prefix  in used the submitted value will be directly executed by Powershell.
- ```:: sys_info``` Collects username, hostname, domain, and local IP
- ```:: enable_persistence``` Enables persistence by embedding a stager payload into the following autorun register key:
   - HKCU:\Software\Microsoft\Windows\CurrentVersion\Run\
- ```:: export_clipboard``` Attempts to collect any text data stored in the users clipboard.
- ```:: load_module [target script]``` This will load external powershell modules, such as JAWS.
- ```:: exec_module [loaded module name]``` Executes a specific function of a loaded module.
- ```:: list_modules``` Lists all loaded modules by the implant.

### Contributing
All contributions, suggestions, and feature requests are welcome.


### License
The FudgeC2 project and all module are under the GNU General Public License v3.0 unless explicitly noted otherwise. You can find the full licence [here](/LICENCE.txt)