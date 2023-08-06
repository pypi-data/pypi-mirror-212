# Mail Notification

## requirements

For running this, you need to have `python3` installed on your system.


## Installation

```
pip3 install mouritech-mail-notification (OR)
pip3 install mouritech-mail-notification --extra-index-url https://__token__:<your_personal_token>@gitlab.mouritech.com/api/v4/projects/339/packages/pypi/simple

link : https://gitlab.mouritech.com/mt-digital-core-platform/python/mail-notification/-/packages/142

```

## Example

1. Mail Configuration

    ```
    from mail_notification import MailConfig
   
    conn = MailConfig(mail_user= 'mail_ID', password='Password')
    ```
   
    MailConfig supported Parameters 
    * mail_user - Mail address(Required)
    * password - Password of the mail(Required)
    * host - (optional) Default value is "smtp.gmail.com"
 
   
2. Send a mail
   
    ```
    conn.send_mail(to_mail='to_mail', subject="mail subject", body="body", body_type='html')
   
    ```
   send_mail supported Parameters 
    * to_mail - Mail address(Required) (accepts "," separated values)
    * subject - subject of the mail(Required)
    * body - body of the mail(Required) (Supports string value only)
    * body_type - supports two values(Required) (plain/html)
                  plain - "hello"
                  html  - "<a>hello<a>"
                                       
    * cc - cc of the mail(Optional)
    * bcc - bcc of the mail(Optional)  
      


3. To close the connection 

    ```
    conn.close_conn()
   
    ```

   

