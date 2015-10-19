#!/usr/bin/env python
# encoding: utf-8

import requests
from lxml import etree

request = u"""<?xml version="1.0" encoding="utf-8"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <soapenv:Header>
    <ebl:RequesterCredentials soapenv:mustUnderstand="0" xmlns:ns="urn:ebay:apis:eBLBaseComponents"
        xmlns:ebl="urn:ebay:apis:eBLBaseComponents">
      <ebl:NotificationSignature xmlns:ebl="urn:ebay:apis:eBLBaseComponents">Z2yhKdKmS0Ga5VPmLDOAlg==</ebl:NotificationSignature>
    </ebl:RequesterCredentials>
  </soapenv:Header>
  <soapenv:Body>
    <GetItemResponse xmlns="urn:ebay:apis:eBLBaseComponents">
      <Timestamp>2008-02-13T03:47:28.106Z</Timestamp>
      <Ack>Success</Ack>
      <CorrelationID>137541140</CorrelationID>
      <Version>553</Version>
      <Build>e553_core_Bundled_6057805_R1</Build>
      <NotificationEventName>ItemSold</NotificationEventName>
      <RecipientUserID>Seller1</RecipientUserID>
      <Item>
        <AutoPay>false</AutoPay>
        <BuyerProtection>ItemEligible</BuyerProtection>
        <BuyItNowPrice currencyID="USD">10.0</BuyItNowPrice>
        <Country>US</Country>
        <Currency>USD</Currency>
        <GiftIcon>0</GiftIcon>
        <HitCounter>NoHitCounter</HitCounter>
        <ItemID>250000627102</ItemID>
        <ListingDetails>
          <Adult>false</Adult>
          <BindingAuction>false</BindingAuction>
          <CheckoutEnabled>true</CheckoutEnabled>
          <ConvertedBuyItNowPrice currencyID="USD">10.0</ConvertedBuyItNowPrice>
          <ConvertedStartPrice currencyID="USD">1.0</ConvertedStartPrice>
          <ConvertedReservePrice currencyID="USD">0.0</ConvertedReservePrice>
          <HasReservePrice>false</HasReservePrice>
          <StartTime>2008-02-13T03:42:45.000Z</StartTime>
          <EndTime>2008-02-13T03:43:32.000Z</EndTime>
          <ViewItemURL>http://cgi.qa-api012.qa.ebay.com/ws/eBayISAPI.dll?ViewItem&amp;item=250000627102&amp;category=1463</ViewItemURL>
          <HasUnansweredQuestions>false</HasUnansweredQuestions>
          <HasPublicMessages>false</HasPublicMessages>
          <ExpressListing>false</ExpressListing>
          <ViewItemURLForNaturalSearch>http://cgi.qa-api012.qa.ebay.com/Test-Item-Won-Sold-notify_W0QQitemZ250000627102QQcategoryZ1463QQcmdZViewItem</ViewItemURLForNaturalSearch>
        </ListingDetails>
        <ListingDuration>Days_5</ListingDuration>
        <ListingType>Chinese</ListingType>
        <Location>San Jose, CA</Location>
        <PaymentMethods>PaymentSeeDescription</PaymentMethods>
        <PaymentMethods>PayPal</PaymentMethods>
        <PayPalEmailAddress>ve2@aol.com</PayPalEmailAddress>
        <PrimaryCategory>
          <CategoryID>1463</CategoryID>
          <CategoryName>Collectibles:Trading Cards:Phone Cards</CategoryName>
        </PrimaryCategory>
        <PrivateListing>false</PrivateListing>
        <Quantity>1</Quantity>
        <ReservePrice currencyID="USD">0.0</ReservePrice>
        <ReviseStatus>
          <ItemRevised>false</ItemRevised>
        </ReviseStatus>
        <Seller>
          <AboutMePage>false</AboutMePage>
          <Email>seller@email.com</Email>
          <FeedbackScore>100</FeedbackScore>
          <PositiveFeedbackPercent>98.1</PositiveFeedbackPercent>
          <FeedbackPrivate>false</FeedbackPrivate>
          <FeedbackRatingStar>Turquoise</FeedbackRatingStar>
          <IDVerified>false</IDVerified>
          <eBayGoodStanding>true</eBayGoodStanding>
          <NewUser>false</NewUser>
          <RegistrationDate>2004-02-23T23:50:13.000Z</RegistrationDate>
          <Site>US</Site>
          <Status>Confirmed</Status>
          <UserID>Seller1</UserID>
          <UserIDChanged>false</UserIDChanged>
          <UserIDLastChanged>2004-02-23T23:48:54.000Z</UserIDLastChanged>
          <VATStatus>NoVATTax</VATStatus>
          <SellerInfo>
            <AllowPaymentEdit>true</AllowPaymentEdit>
            <CheckoutEnabled>true</CheckoutEnabled>
            <CIPBankAccountStored>false</CIPBankAccountStored>
            <GoodStanding>true</GoodStanding>
            <MerchandizingPref>OptIn</MerchandizingPref>
            <QualifiesForB2BVAT>false</QualifiesForB2BVAT>
            <SellerLevel>None</SellerLevel>
            <StoreOwner>false</StoreOwner>
            <ExpressEligible>false</ExpressEligible>
            <ExpressWallet>false</ExpressWallet>
            <SafePaymentExempt>true</SafePaymentExempt>
          </SellerInfo>
          <MotorsDealer>false</MotorsDealer>
        </Seller>
        <SellingStatus>
          <BidCount>2</BidCount>
          <BidIncrement currencyID="USD">0.25</BidIncrement>
          <ConvertedCurrentPrice currencyID="USD">1.25</ConvertedCurrentPrice>
          <CurrentPrice currencyID="USD">1.25</CurrentPrice>
          <HighBidder>
            <AboutMePage>false</AboutMePage>
            <EIASToken>nY+sHZ2PrBmdj6wVnY+sEZ2PrA2dj6wJkoWoCJaGoAmdj6x9nY+seQ==</EIASToken>
            <Email>buyer@email.com</Email>
            <FeedbackScore>5</FeedbackScore>
            <PositiveFeedbackPercent>100.0</PositiveFeedbackPercent>
            <FeedbackPrivate>false</FeedbackPrivate>
            <FeedbackRatingStar>None</FeedbackRatingStar>
            <IDVerified>false</IDVerified>
            <eBayGoodStanding>true</eBayGoodStanding>
            <NewUser>false</NewUser>
            <RegistrationDate>2004-02-24T07:00:00.000Z</RegistrationDate>
            <Site>US</Site>
            <Status>Confirmed</Status>
            <UserID>Buyer1</UserID>
            <UserIDChanged>false</UserIDChanged>
            <UserIDLastChanged>2004-02-24T07:00:00.000Z</UserIDLastChanged>
            <VATStatus>NoVATTax</VATStatus>
            <BuyerInfo>
              <ShippingAddress>
                <Country>US</Country>
                <PostalCode>95125</PostalCode>
              </ShippingAddress>
            </BuyerInfo>
            <UserAnonymized>false</UserAnonymized>
          </HighBidder>
          <LeadCount>0</LeadCount>
          <MinimumToBid currencyID="USD">1.5</MinimumToBid>
          <QuantitySold>1</QuantitySold>
          <ReserveMet>true</ReserveMet>
          <SecondChanceEligible>true</SecondChanceEligible>
          <ListingStatus>Completed</ListingStatus>
        </SellingStatus>
        <ShippingDetails>
          <AllowPaymentEdit>true</AllowPaymentEdit>
          <ApplyShippingDiscount>false</ApplyShippingDiscount>
          <InsuranceOption>NotOffered</InsuranceOption>
          <SalesTax>
            <SalesTaxPercent>0.0</SalesTaxPercent>
            <ShippingIncludedInTax>false</ShippingIncludedInTax>
          </SalesTax>
          <ThirdPartyCheckout>false</ThirdPartyCheckout>
          <TaxTable/>
        </ShippingDetails>
        <ShipToLocations>US</ShipToLocations>
        <Site>US</Site>
        <StartPrice currencyID="USD">1.0</StartPrice>
        <TimeLeft>PT0S</TimeLeft>
        <Title>Test Item{Won/Sold} notify</Title>
        <HitCount>0</HitCount>
        <GetItFast>false</GetItFast>
        <PostalCode>
        </PostalCode>
        <PictureDetails>
          <PhotoDisplay>None</PhotoDisplay>
        </PictureDetails>
        <ProxyItem>false</ProxyItem>
      </Item>
    </GetItemResponse>
  </soapenv:Body>
</soapenv:Envelope>"""

# request = u"""<?xml version="1.0" encoding="utf-8"?>
# <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
#   <soapenv:Body>
#     <GetItemResponse xmlns="urn:ebay:apis:eBLBaseComponents">
#       <Ack>Success</Ack>
#     </GetItemResponse>
#   </soapenv:Body>
# </soapenv:Envelope>"""



encoded_request = request.encode('utf-8')

print "*"*10
print "*"*10 + " REQUEST " + "*"*10
print "*"*10
print encoded_request
print "*"*10 + "\n\n"

headers = {"Host": "localhost",
           "Content-Type": "text/xml; charset=UTF-8",
           "Content-Length": len(encoded_request),
           "SOAPAction": "https://developer.ebay.com/notification/ItemSold",
           }

response = requests.post(url="http://localhost:8008/",
                         headers = headers,
                         data = encoded_request,
                         verify=False)

# print unicode(etree.fromstring(response.text))
print "*"*10
print "*"*10 + " RESPONSE " + "*"*10
print "*"*10
print response.text
print "*"*10 + "\n\n"
