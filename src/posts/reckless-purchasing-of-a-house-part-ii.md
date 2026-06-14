---
title: "Reckless purchasing of a house – Part II"
date: 2022-07-09
categories:
  - "Personal"
summary: "The aftermath of a too-fast house purchase — repairs, regrets, and all."
hero: "/images/posts/reckless-purchasing-of-a-house-part-ii/hero.png"
---

This is part II of the “how not to buy a house in a week” trilogy. Read [part I](https://timtianchen.wordpress.com/2022/05/30/reckless-purchasing-of-a-house-part-i/) first.

#### Day 8

The morning of, we wrote down a detailed list of things that needed fixing, the approximate cost of fixing these things, provided references for each items. Feeling pretty confident with the number, we went and met our agent in his apartment to go through the list and draft an email to the sellers asking for money.

There are several items that were clearcut, things like 1) the water boiler is long expired (5 years beyond the intended 10 years usage) and needs to be replaced, 2) some ceiling insulation is missing (as shown on a infrared camera), 3) wall outlets that do not have a *ground-fault circuit interrupter* (GFCI) near the kitchen / bathroom / garage. There were other things that were hazardous, 1) the wooden canopy on the terrace is rotting away, 2) the fence in the driveway is about to fall down, 3) the faucet in the master bathtub output brown water. Then there are things that are questionable, hairline cracks, incorrect electrical box arrangement, and so on.

We added up the items that we thought were necessary, and asked for around \$15k. Later that day, we got a passive aggressive email that threw our list of demand into the bin. We went back and forth a bit and got around \$3k in reimbursements. Looking back at it, I do not know how we could have extracted more.

**Day 9**

The inspector suggested that someone trim the hedge around the electric box where the main power supply line from the street goes into the house so he could see the wiring without being electrocuted. The owners relented after some grumbling. Somehow, the husband fell when he was doing this, and had to get stitches on his face. That stopped the trimming, but the inspector was kind enough to visit the property again to check out that box.

**Day 10**

We engaged two different mortgage lenders to get quotes and rates. Since I had, at that point, lived in the States for less than 2 years, nothing worked. The lenders asked for every single minuscule detail of my financial background. Fortunately, my credit rating was just sufficient to get something. And with the promise of a massive (36%) down payment, they agreed to extend me a loan for the remainder (~\$300,000) at a rate of 4.875% over 15 years.

This rate was already about 2% higher than January, a mere 4 months ago, and now (July) it’s around 5.25%.

**Day 12**

With that, the get-out-the-deal time period elapsed and we were in it for good.

**Day 14**

My aunt, through my dad, asked me if we needed money. The answer was, clearly, yes we needed money. She was willing to lend us a supplementary amount (~\$230,000) at a 4% rate over 15 years. The actual operation of money transfer took some tricky banking operations and a trip back to Canada.

**Day 16**

I hadn’t been back to Canada since January of 2019. 2 and three years later, after a brief stint in the States, I’ve come to appreciate how nice Canada was. After landing at Toronto Pearson, I went directly to the bank. This was an extra-ordinary behavior on my part, since I always make a bee-line to a near by Tim Hortons. I needed this wire transfer to go through, and banks get very difficult when such a large amount is transferred internationally.

**Day 18**

As a part of the mortgage lending process. The appraisal came back with a number lower than our offer. This was a disappointment, since we wanted to see the house being more worthy than the amount we are offering. Though, it did seem like a blessing in disguise since now the mortgage lender could potentially back out of the deal, and we then would have no choice but to back out of the offer. We were within the 21 days and there would be no penalty (except the options fee). Armed with this we asked the sellers to reduce the total by \$5,661, surprisingly they obliged. This was interesting, because this is one of the few opportunities we get to back out of the deal after the options period. We may have been able to ask for more, since this far in, the sellers are invested in making it through.

**Day 36**

The mortgage calculation (U.S. specific) follows a simple set of equations. The calculation ensures that the lenders pays the exact same amount every month in the entire loan period. The payment per month *c* can be calculated using the following equation, note that this will be the monthly payment through the entire loan period.

![](/images/posts/reckless-purchasing-of-a-house-part-ii/hero.png)

Where *P* is the principle (the amount of loan we got), *r* is the annual interest rate, *n* is the number of payments per year (in our case, it is 12), and *t* is the loan terms in years. The available terms are 5 years, 10 years, 15 years and 30 years. The yearly rate is largely dictated by the federal treasury or the federal reserve, or the federal bank, or some other people. In Excel, this function is called “PMT”. It calculates the payment for a loan based on constant payments and a constant interest rate. The derivation is given in [Wikipedia](https://en.wikipedia.org/wiki/Compound_interest), and it includes a nifty use of geometric series.

Given *c*, we can calculate the total balance at the beginning of each month, which is simply the previously balance minus *c*. With that total balance, we can calculate the monthly interest, by multiplying the total balance by *r / n*. If we subtract *c* by this monthly interest, we will see how much of the principle we are actually paying off. There are many excel sheets online that you can download to do this calculation for you, but it is always instructive to know how these numbers are gotten. This should be, and was, the exact same amount as what we were given in the Closing Disclosure (CD).

For some historical reasons (*i.e.* the recession of 2008), the U.S. mortgage market became quite heavily regulated. The background checks are quite stringent and the lender has quite some leverage. Things like 15 or 30 year fixed rates are unheard-of in Canada for example. The ability to overpay as much as one wants without penalty is also a benefit that significantly cuts down the total interest payments as we will see below.

The first two plots show our actual loan calculation for a 15 year term without any added monthly payments. In the plot below to the left, the initial payments mostly directed towards the incurred interests, and the latter payments mostly into the principle loan amount. Note that in the first months. half of the monthly payments go towards interest. The plot on the right shows the decrease of the principle amount w.r.t. time, and the incurred total interest.

![](/images/posts/reckless-purchasing-of-a-house-part-ii/screen-shot-2022-07-09-at-09.43.41.png)

Now, if we pay \$52,500 in the first month instead of the actual monthly bill of ~\$2,500, we cut down the total interest payment (by the conclusion of the loan) by \$42,000. We also reduce the total loan term by about 5 years. The following two plots show this.

![](/images/posts/reckless-purchasing-of-a-house-part-ii/screen-shot-2022-07-09-at-09.46.07.png)

**Day 37**

The Closing Disclosure (CD) was a document that the mortgage lender sent us many times over. They generated a new one every time numbers change, and force us to sign them online again and again. It was another one of those documents with a simple set of calculations (adding and subtracting) that was made out to be super complex. We made an excel sheet to ensure their calculations were correct. The lender did make mistakes, and it took my multiple harassing emails and calls to ensure they got the numbers right. I don’t know if that was the normal practice and they were just slowly converging to the right numbers, or they were actually incompetent. It was critical to ensure whatever was on the offer letter gets translated to this document, down to the last dollar.

The first page contained all the important quantities including the loan amount (P), the interest rate (r), the monthly payment (c), the projected payments including property taxes, homeowner’s insurance, and HOA dues. I was asked if I wanted to engage with an escrow to pay these projected payments on my behalf. I assume that the mortgage lender would charge me to maintain this escrow, and didn’t find any sense in that. The first page also contained the closing costs and cash to close. The first number contains all the fees the various agencies charged the buyer (us), the second was the amount we had to pay at closing. For our CD, the following items were non-standard and had to be rectified at one point.

- The actual amount of down-payment. This, and not the percentage, matters.
- Title insurance was to be paid by the seller
- Home insurance was paid in advance (for a year) separately
- Seller gave a credit
- Appraisal was pre-paid
- The actual earnest money that was pre-paid

**Day 39**

This was the original date of closing on the offer letter. The mortgage lender had major difficulties with verifying my income from EPFL. We had to reschedule. We were at risk of losing the earnest money, which amounted to about \$25,000. A lot of anxious and panic ridden calls to all parties and haranguing them to get their act together.

**Day 40**

I drove to the title company and signed a stack of documents. That ended this process, and the house was officially ours. It felt anticlimactic since we didn’t physically receive anything. This may not be of much practical value, but I don’t know what we actually bought. I don’t know how much of the “worth” of the house is that plot of land, or the structure on top of that land. I don’t if there can be challenges to the ownership of the land.

I would say that, just like everything else in US bureaucracy or in bureaucracy in general, any deviations from the standard operating procedure created a huge amount of headache. While it would seem that the stack of documents 100 pages thick would be complicated, but the opposite was true. 90% of that could pertain to the purchase of literally any house at all.

**Day \>40**

With the purchase of this house, we automatically became landlords to the tenants currently living in our house. With that the trilogy of two parts end.
