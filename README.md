<div id="badges" align="center">
<h1>Chatbot Repository</h1>
<img src="https://i.gifer.com/7BZk.gif" alt="Frontend Developer" width="200" />
</div>
<p>This repository contains the code with Python and library pyTelegramBotAPI for a Telegram chatbot.
    The bot interacts with users and includes an admin feature that allows you to manage it through Telegram using your unique user ID. 
  To use the admin features, you need to provide your Telegram token and your Telegram user ID.</p>
<h2>Requirements</h2>
<p>Before you start, ensure you have the following:</p>
<ul align="left">
  <li>Python 3.x</li>
  <li>pip (Python package manager)</li>
</ul>
<h2>Setup</h2>
<b>1. Clone the repository</b>
  <p>First, clone the repository to your local machine:</p>
  <pre class="notranslate">
    <code>git clone https://github.com/yourusername/chatbot-repo.git</code>
  </pre>
  <pre class="notranslate">
    <code>cd chatbot-repo</code>
  </pre>
<b>2. Install dependencies</b>
  <p>Install the required dependencies using pip:</p>
  <pre class="notranslate">
    <code>pip install -r requirements.txt</code>
  </pre>
<b>3. Create a .env file</b>
  <p>Create a .env file in the root directory of the repository. You can do this manually or run the following command:</p>
  <pre class="notranslate">
    <code>touch .env</code>
  </pre>
<b>4. Add your Telegram Bot Token and User ID</b>
  <p>Open the .env file and add the following information:</p>
  <pre class="notranslate">
    <code>TELEGRAM_TOKEN=your_telegram_bot_token
      ADMIN_ID=your_telegram_user_id
    </code>
	</pre>
<ul>
  <li>Replace <em>your_telegram_bot_token</em> with the token you received from <a href="https://gerabot.com/ru/article/botfather_mozhlivosti_ta_funkcional">BotFather</a> on Telegram.</li>
  <li>Replace <em>your_telegram_user_id</em> with your unique Telegram user ID. This is required to grant you admin privileges.</li>
</ul>

<p>The bot will start running, and you can interact with it on Telegram. Only the user with the specified ADMIN_ID will have admin privileges.</p>
