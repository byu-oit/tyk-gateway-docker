variable "env" {
  type = string
}

module "acs" {
  source = "github.com/byu-oit/terraform-aws-acs-info?ref=v3.2.0"
}

data "aws_route53_zone" "zone" {
  name = "api-${var.env}.byu.edu."
}

resource "aws_acm_certificate" "cert" {
  domain_name               = "api-${var.env}.byu.edu"
  subject_alternative_names = ["*.api-${var.env}.byu.edu"]
  validation_method         = "DNS"
}

resource "aws_route53_record" "cert_validation" {
  for_each = {
    for dvo in aws_acm_certificate.cert.domain_validation_options : dvo.domain_name => {
      name   = dvo.resource_record_name
      record = dvo.resource_record_value
      type   = dvo.resource_record_type
    }
  }

  allow_overwrite = true
  name            = each.value.name
  type            = each.value.type
  zone_id         = data.aws_route53_zone.zone.zone_id
  records         = [each.value.record]
  ttl             = 60
}

resource "aws_acm_certificate_validation" "cert" {
  certificate_arn         = aws_acm_certificate.cert.arn
  validation_record_fqdns = [for record in aws_route53_record.cert_validation : record.fqdn]
}

resource "aws_iam_user" "tyk" {
  name                 = "tyk"
  permissions_boundary = module.acs.user_permissions_boundary.arn
}

resource "aws_iam_access_key" "tyk" {
  user = aws_iam_user.tyk.name
}

resource "aws_iam_user_policy" "tyk-s3" {
  name = "tyk-s3"
  user = aws_iam_user.tyk.name

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
        "Effect": "Allow",
        "Action": [
          "s3:CreateBucket",
          "s3:ListBucket",
          "s3:GetBucketLocation",
          "s3:DeleteBucket"
        ],
        "Resource": "arn:aws:s3:::mserv-plugin-*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "s3:PutObject",
        "s3:GetObject",
        "s3:DeleteObject"
      ],
      "Resource": "arn:aws:s3:::mserv-plugin-*/*"
    }
  ]
}
EOF
}

