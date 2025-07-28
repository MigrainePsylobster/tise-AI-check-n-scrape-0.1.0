Description:
Make a app / scrip that will run on windows.
The app will check the clothing website "Tise.com" and mainly on profiles i want my script to check.
Script will check x time often and look if a new post is made.
If new post is made, it will check post and if it has not been downloaded before it should download
When post is checked and it exist already (aka already downloaded), SKIP


Lang:
Python Perferd, but ok with other languages also, i just need to learn them


questions:
best check option ?
how often should it check
best to save and check a win folder or integrade database ?


New Notes:
I want it to run in a python enviorment, and make one on if need, then install requierments.

### 3. **Checking Frequency**
**Questions**:
- How active are the profiles you're monitoring?
- Are you looking for real-time updates or is a delay acceptable?

**Suggestions**:
- Start with **15-30 minutes intervals** to avoid being blocked
- Implement **exponential backoff** if no new content is found
- Add **random delays** between requests to appear more human-like

New note 2, i want do some practial stuff to learn.
For example adding venv and  etc


new notes 4.
folder for images and data should be controlled by username, so i can have multiple profiles and only connected correct data