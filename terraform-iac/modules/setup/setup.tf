variable "env" {
  type = string
}

variable "portal_url" {
  type = string
}

variable "dashboard_url" {
  type = string
}

variable "west_gw_url" {
  type = string
}

variable "east_gw_url" {
  type = string
}

variable "provo_gw_url" {
  type = string
}

resource "aws_route53_zone" "zone" {
  name = "api-${var.env}.byu.edu"
}

resource "aws_route53_record" "portal" {
  name    = "portal.api-${var.env}.byu.edu"
  type    = "CNAME"
  ttl     = 300
  zone_id = aws_route53_zone.zone.id
  records = [var.portal_url]
}

resource "aws_route53_record" "dashboard" {
  name    = "dashboard.api-${var.env}.byu.edu"
  type    = "CNAME"
  ttl     = 300
  zone_id = aws_route53_zone.zone.id
  records = [var.dashboard_url]
}

resource "aws_route53_record" "gateway" {
  name    = "gateway.api-${var.env}.byu.edu"
  type    = "CNAME"
  ttl     = 300
  zone_id = aws_route53_zone.zone.id
  records = [
    var.west_gw_url,
    var.east_gw_url,
    var.provo_gw_url
  ]
}

output "hosted_zone" {
  value = aws_route53_zone.zone
}
