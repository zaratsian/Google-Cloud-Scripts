<h3>Google Cloud Platform
</h3><!--<img src="" class="inline"/>-->
Collection of Google Cloud Platform Scripts and References 
<br>
<br>
<br><b>GCP Documentation:</b>
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;<a href="https://cloud.google.com/sdk/docs/">GCP SDK</a>
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;<a href="https://cloud.google.com/storage/docs/gsutil">GCP gsutil Commands</a>
<br>
<br>
<br><b><a href="https://cloud.google.com/source-repositories/docs/">Cloud Source Repo</a></b> 
<br><b>Initial Config:</b>
<br>1) <code>gcloud init</code>
<br>2) <code>git config --global user.email "you@example.com"</code>
<br>3) <code>git config --global user.name "Your Name"</code>
<br>4) <code>gcloud source repos clone my_repo_name --project=my_project_id</code>
<br>5) <code>cd my_repo_name</code>
<br>6) <code>...add files to repo...</code>
<br>7) <code>git add myfile.py</code>
<br>8) <code>git commit -m "my comment"</code>
<br>9) <code>git push origin master</code>
<br>
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Create Repo: <code>gcloud source repos create zrepo</code>
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Clone Repo:  <code>gcloud source repos clone zrepo</code>
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Interact w/ repo: repo: Use normal git cmds (ie. git add, git commit, git push)
<br>
