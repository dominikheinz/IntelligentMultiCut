### Git Branches

<b> Alle Branches auflisten (inkl. der eingeloggte)</b>
<pre>git branch -a</pre>  

<b> Branch hinzufügen</b>
<pre>git checkout -b branch_name</pre>

<b> Auf Branch switchen</b>
<pre>git checkout branch_name</pre>

<b> Von eigenem Branch pushen</b>
<pre>
git pull origin branch_name
git add .
git commit -m "message"
git push origin branch_name
</pre>

<b> Merge Konflikte beheben (gui)</b>
<pre>git mergetool</pre>

https://stackoverflow.com/questions/67699/how-to-clone-all-remote-branches-in-git
