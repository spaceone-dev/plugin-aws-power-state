# plugin-aws-power-state

Plugin for AWS Power State
- Collecting Instance State
- Collecting RDS Instance State
- Collecting Auto Scaling Group State

# Data Sample

## EC2

~~~
"data": {
	"compute": {
		"instance_state": "RUNNING",
			...
		},
	"power_state": {
		"instance_state": "passed",
		"system_state": "passed"
	},

	....
		
}
~~~
	
