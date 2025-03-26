#!/bin/bash

public_key="MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAjNZgeWB6Wmcyar0RA15cY2kiIzCHL+3CFx2oLuU7yd11GkZSfFNLIQwc716h9VWPSF9AimzmwBFMtYoj1iZzBdZdzIu6qoGfMpeI1O2IlrHGio548hI08d0TYzKXHSNGE2ZlXj2a6JMdSdn4r47xwqUXWNAkHr0o8HPk+vSft2R/fDBGkDfX2z/g73J3zJX/BTSAnzi9NGfaTV3eiVQnhJn0UMfTK5E3jT7fSoRSMWa1qTK9ClONeob5eBfXcntjiazuAwB1DB7hFMQYYg0y4AjpnvFZP3S0goYApBqNqz73L2fALZLTy3JIaTpWIWfGYJjyC1oOKvPCqIkd5rXgXwIDAQAB"

profile_picture_url="https://images.pexels.com/photos/177809/pexels-photo-177809.jpeg?auto=compress&cs=tinysrgb&w=1200"

curl -X POST \
  http://localhost:3000/register \
  -H "Content-Type: application/json" \
  -d "{
    \"username\": \"test123\",
    \"public_key\": \"$public_key\",
    \"profile_picture_url\": \"$profile_picture_url\"}"