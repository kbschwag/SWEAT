<?php
if(isset($_POST['email'])) {

    // EDIT THE FOLLOWING LINES AS REQUIRED
    $email_to = "sweatsiteofficial@gmail.com"; // your email address
    $email_subject = "New message from website contact form";

    function died($error) {
        // your error code can go here
        echo "We are very sorry, but there were error(s) found with the form you submitted. ";
        echo "These errors appear below.<br /><br />";
        echo $error."<br /><br />";
        echo "Please go back and fix these errors.<br /><br />";
        die();
    }

    // validation expected data exists
    if(!isset($_POST['email']) ||
        !isset($_POST['recipient_email']) ||
        !isset($_POST['message'])) {
        died('We are sorry, but there appears to be a problem with the form you submitted.');
    }

    $email_from = $_POST['email']; // sender's email address
    $recipient_email = $_POST['recipient_email']; // recipient's email address
    $message = $_POST['message']; // message content

    $error_message = "";
    $email_exp = '/^[A-Za-z0-9._%-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}$/';

    if(!preg_match($email_exp,$email_from)) {
        $error_message .= 'The Email Address you entered does not appear to be valid.<br />';
    }

    if(!preg_match($email_exp,$recipient_email)) {
        $error_message .= 'The recipient Email Address you entered does not appear to be valid.<br />';
    }

    if(strlen($message) < 2) {
        $error_message .= 'The message you entered do not appear to be valid.<br />';
    }

    if(strlen($error_message) > 0) {
        died($error_message);
    }

    $email_message = "Form details below.\n\n";

    function clean_string($string) {
        $bad = array("content-type","bcc:","to:","cc:","href");
        return str_replace($bad,"",$string);
    }

    $email_message .= "Sender's Email: ".clean_string($email_from)."\n";
    $email_message .= "Recipient's Email: ".clean_string($recipient_email)."\n";
    $email_message .= "Message: ".clean_string($message)."\n";

    // create email headers
    $headers = 'From: '.$email_from."\r\n".
        'Reply-To: '.$email_from."\r\n" .
        'X-Mailer: PHP/' . phpversion();

    // send email to your email address
    mail($email_to, $email_subject, $email_message, $headers);

    // send email to recipient's email address
    mail($recipient_email, $email_subject, $email_message, $headers);

?>

<!-- Success message -->
<!DOCTYPE html>
<html>
<head>
	<title>Thank You</title>
	<link rel="stylesheet" type="text/css" href="style.css">
</head>
<body>
	<div class="container">
		<h1>Thank You</h1>
		<p>Your message has been sent.</p>
	</div>
</body>
</html>

<?php
}
?>