# Create a Step_function and add below script to trigger the ssh_keys and update-keys-in-ec2 lambda functions.
{
  "Comment": "Generate and deploy SSH key to EC2",
  "StartAt": "ssh-keys",
  "States": {
    "ssh-keys": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:us-west-2:732940909765:function:ssh-keys",
      "Next": "update-keys-in-ec2"
    },
    "update-keys-in-ec2": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:us-west-2:732940909765:function:update-keys-in-ec2",
      "End": true
    }
  }
}
