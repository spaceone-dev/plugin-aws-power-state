# plugin-aws-power-state

Plugin for AWS Power State
- Collecting Instance State
- Collecting RDS Instance State
- Collecting Auto Scaling Group State

# Data Sample

## EC2

~~~
"data": {
	"power_state": {
		"status": "RUNING" | "STOPPED" | "UNHEALTHY" | "IN_PROGRESS"
	},

	....
		
}
~~~

## Auto Scaling Group

- cloud_service_type: AutoScalingGroup
- cloud_service_group: AutoScaling
- provider: aws

~~~
'data': {
	'auto_scaling_group_arn': 'arn:aws:autoscaling:ap-northeast-2:257706363616:autoScalingGroup:0c9774b0-c96a-4cea-9326-e1f3acfd6eec:autoScalingGroupName/eks-c2b977fd-fb2c-2e2f-fbac-f9ea109b1d89',
	'auto_scaling_group_name': 'eks-c2b977fd-fb2c-2e2f-fbac-f9ea109b1d89',
	'desired_capacity': 8.0,
	'max_size': 10.0,
	'min_size': 8.0
	'instances': [{'availability_zone': 'ap-northeast-1c',
                       'health_status': 'Healthy',
                       'instance_id': 'i-0004606c1e4386ff8',
                       'instance_type': 't2.nano',
                       'launch_template': {'launch_template_id': 'lt-00f3ed190ed130592',
                                           'launch_template_name': 'power-scheduler-test-by-choonho',
                                           'version': '1'},
                       'lifecycle_state': 'InService',
                       'lifecycle': 'spot' | 'schedule', 
                       'protected_from_scale_in': False}, ...
	]
	},

~~~

## RDS

- cloud_service_type: Database
- cloud_service_group: RDS
- provider: aws

~~~
'data': {
	'arn': 'arn:aws:rds:us-east-1:257706363616:db:terraform-20200811083041083200000001',
        'db_identifier': 'terraform-20200811083041083200000001',
	'role': 'instance',
	'status': 'stopping'
	...
	}
~~~

