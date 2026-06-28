# Federated Learning of Cohorts

Source: Wikipedia (https://en.wikipedia.org/wiki/Federated_Learning_of_Cohorts)

Federated Learning of Cohorts (FLoC) is a type of web tracking. It groups people into "cohorts" based on their browsing history for the purpose of interest-based advertising. FLoC was being developed as a part of Google's Privacy Sandbox initiative, which includes several other advertising-related technologies with bird-themed names. Despite "federated learning" in the name, FLoC does not utilize any federated learning.
Google began testing the technology in Chrome 89 released in March 2021 as a replacement for third-party cookies. By April 2021, every major browser aside from Google Chrome that is based on Google's open-source Chromium platform had declined to implement FLoC. The technology was criticized on privacy grounds by groups including the Electronic Frontier Foundation and DuckDuckGo, and has been described as anti-competitive; it generated an antitrust response in multiple countries as well as questions about General Data Protection Regulation compliance. In July 2021, Google quietly suspended development of FLoC; Chrome 93, released on August 31, 2021, became the first version which disabled FLoC, but did not remove the internal programming.
On January 25, 2022, Google officially announced it had ended development of FLoC technologies and proposed the new Topics API to replace it. Brave developers criticized Topics API as a rebranding of FLoC with only minor changes and without addressing their main concerns.


== Function ==

The Federated Learning of Cohorts algorithm analyzes users' online activity within the browser, and generates a "cohort ID" using the SimHash algorithm to group a given user with other users who access similar content. Each cohort contains several thousand users in order to make identifying individual users more difficult, and cohorts are updated weekly. Websites are then able to access the cohort ID using an API and determine what advertisements to serve. Google does not label cohorts based on interest beyond grouping users and assigning an ID, so advertisers need to determine the user types of each cohort on their own.


=== Opting out of cohort calculation ===
FLoC experiment was active only in Google Chrome browser and ran from Chrome 89 (inclusive) to Chrome 93 (not inclusive). Modern browsers do not support FLoC. While the experiment was active, users could opt out of FLoC experiment by disabling third-party cookies. Website administrators could opt out from cohort calculation via special HTTP headers. It can be accomplished with a new interest-cohort permissions policy or feature policy, the default behavior is to allow cohort calculation. To opt-out of all FLoC cohort calculations a website could send either of the following HTTP response headers:

Permissions-Policy: browsing-topics=()

or

Feature-Policy: browsing-topics 'none'

Google Chrome applies interest-cohort Feature Policy restrictions to Browsing Topics API as well.


== Timeline ==


=== Initial prototype ===
On August 22, 2019, Google Chrome developers coined the term FLoC and first started discussing the upcoming replacement for cookies. In July 2020, the United Kingdom's Competition and Markets Authority found the FLoC proposal to be anti-competitive, since it would "place the browser in a vital gatekeeper position for the adtech ecosystem." Instead, the authority recommended adoption of a competing proposal called SPARROW, which maintains the same privacy-enhancing objectives but creates a different completely independent "Gatekeeper" which does not have any other role in the adtech ecosystem and does not have access to user-level information.


=== Testing ===
Google began testing FLoC in the Chrome 89 released in March 2021 as a replacement for third-party cookies, which Google plans to stop supporting in Chrome by mid-2023. (Initially Google announced plans to remove third-party cookies by late 2021, then postponed it to early 2022, and then to 2023 due to delay of FLoC technology.) The initial trial turned on FLoC for 0.5% of Chrome users across 10 countries: the United States, Australia, Brazil, Canada, India, Indonesia, Japan, Mexico, New Zealand and the Philippines. Users were automatically placed in the trial and were not notified, but could opt out by turning off third-party cookies. Furthermore, site administrators could disable FLoC and opt out from interest calculation via a Feature-Policy header. The initial trial did not include users in the United Kingdom or the European Economic Area due to concerns about legality under the area's privacy regulations.


=== FLoC shutdown ===
In July 2021, Google suspended development of FLoC; Chrome 93, released on August 31, 2021, became the first version which rendered FLoC feature void, but did not remove the internal programming. Chrome 100, released on March 29, 2022, removed most of old FLoC code. 


=== Topics API ===
On January 25, 2022, Google officially announced it had ended development of FLoC APIs and proposed a new Topics API to replace it. This API would use three weeks of the browser's history to identify user interests based on defined topics (referred to as "IAB Content Taxonomy"). Participating websites could then call this API to get three topics (items from "IAB Content Taxonomy") which could be used to tailor advertising. Developers of the Brave web browser called Topics API a "rebranding [of] FLoC without addressing key privacy issues. On Oct 17, 2025, Google published a blog post deprecating most of Privacy Sandbox technologies, including Topics API.
From February to April 2026, Google engineers were prototyping yet another API based on "IAB Content Taxonomy". Originally the functionality was referred to as "Taxonomy API" until being renamed to "Classifier API". Under the new scheme, Chrome would get a new API which would take some free-form text as input and output IAB Taxonomy labels and associated confidences for it. The On April 19 2026, Google engineer stated the API is "no longer pursued due to insufficient signals of interest".
In June of 2026, Google Chrome 150 will be released and will disable Topics API and associated controls in settings for majority of users.


== Reactions ==
Google claimed in January 2021 that FLoC was at least 95% effective compared to tracking using third-party cookies, but AdExchanger reported that some people in the advertising technology industry expressed skepticism about the claim and the methodology behind it. As every website that opts into FLoC will have the same access about which cohort the user belongs to, the technology's developers say this democratizes access to some information about a user's general browser history, in contrast to the status quo, where websites have to use tracking techniques.
The Electronic Frontier Foundation has criticized FLoC, with one EFF researcher calling the testing of the technology in Chrome "a concrete breach of user trust in service of a technology that should not exist" in a post on the organization's blog. The EFF also created a website which allows Chrome users to check whether FLoC is being tested in their browsers. The EFF criticized the fact that every site will be able to access data about a user, without having to track them across the web first. Additionally on the EFF blog, Cory Doctorow praised Chrome's planned removal of third-party cookies, but added that "[just] because FLoC is billed as pro-privacy and also criticized as anti-competitive, it doesn't mean that privacy and competition aren't compatible", stating that Google is "appointing itself the gatekeeper who decides when we're spied on while skimming from advertisers with nowhere else to go."
On April 10, 2021, the CEO of DuckDuckGo released a statement telling people not to use Google Chrome, stating that Chrome users can be included in FLoC without choosing to be and that no other browser vendor has expressed interest in using the tracking method. The statement said that "there is no such thing as a behavioral tracking mechanism imposed without consent that respects people's privacy" and that Google should make FLoC "explicitly opt-in" and "free of dark patterns". DuckDuckGo also announced that its website will not collect FLoC IDs or use them to target ads, and updated its Chrome extension to block websites from interacting with FLoC.
On April 12, 2021, Brave, a web browser built on the Chromium platform, criticized FLoC in a blog post and announced plans to disable FLoC in the Brave browser and make company's main website opt out of FLoC. The blog post, co-written by the company's CEO Brendan Eich, described Google's efforts to replace third-party cookies as "Titanic-level deckchair-shuffling" and "a step backward from more fundamental, privacy-and-user focused changes the Web needs."
Tech and media news site The Verge noted that not all possible repercussions of FLoC for ad tech are known, and that its structure could benefit or harm smaller ad tech companies, noting specifically that larger ad tech companies may be better equipped to "parse what FLoCs mean and what ads to target against them."
Multiple companies including GitHub, Drupal and Amazon declined to enable FLoC, instead opting to disable FLoC outright by including the HTTP Header Permissions-Policy: interest-cohort=(). WordPress, a widely used website framework floated a proposal to disable FLoC based tracking across all websites that used the framework.
Almost all major browsers based on Google's open-source Chromium platform declined to implement FLoC, including Microsoft Edge, Vivaldi, Brave, and Opera.
In May 2021, The Economist reported that it may be hard for Google to "stop the system from grouping people by characteristics they wish to keep private, such as race or sexuality."


=== Fingerprinting concerns ===
In May 2021, The Economist said some critics have suggested that the cohort system will facilitate fingerprinting of individual devices, compromising privacy.
Wired magazine additionally reported that FLoC could "be used as a point of entry for fingerprinting".
Mozilla, the creators of the Firefox browser, expressed concerns that FLoC can be used as an additional fingerprinting vector. Furthermore, they stated that a user's FLoC group can be tracked during multiple visits and correlated via different means and, based on a user's membership in multiple FLoC cohorts, a website might be able to infer information about the user which FLoC aimed to keep private. Since a FLoC cohort is shared across websites, its ID might be abused as an alternative to a unique cookie in third-party contexts.


=== Antitrust response ===
In July 2020, the United Kingdom's Competition and Markets Authority found that the FLoC proposal "place[s] the browser in a vital gatekeeper position for the adtech ecosystem."
In March 2021, 15 attorneys general of U.S. states and Puerto Rico amended an antitrust complaint filed in December; the updated complaint says that Google Chrome's phase-out of third-party cookies in 2022 will "disable the primary cookie-tracking technology almost all non-Google publishers currently use to track users and target ads. Then [...] Chrome, will offer [...] new and alternative tracking mechanisms [...] dubbed Privacy Sandbox. Overall, the changes are anticompetitive".
In June 2021, EU antitrust regulators launched a formal investigation to assess whether Google violated competition rules, with a focus on display advertising, notably whether it restricts access to user data by third parties while reserving it for its own use. Among the things that will be investigated is Google's plan to prohibit the placement of third-party cookies and replace them with the Privacy Sandbox set of tools.


=== GDPR compliance ===
As of April 2021, Google was not testing FLoC in the United Kingdom or the European Economic Area due to concerns about compliance with the General Data Protection Regulation and the ePrivacy Directive.
Johannes Caspar, the Data Protection Commissioner of Hamburg, Germany, told Wired UK that FLoC "leads to several questions concerning the legal requirements of the GDPR," explaining that FLoC "could be seen as an act of processing personal data" which requires "freely given consent and clear and transparent information about these operations." A spokesperson of the French National Commission on Informatics and Liberty said that the FLoC system would require "specific, informed and unambiguous consent".
As of April 2021, the Irish Data Protection Commission, which is the lead data supervisor for Google under GDPR, was consulting with Google about the FLoC proposal.


== References ==


== External links ==
Am I FLoCed?—EFF website reporting to users if FLoC is enabled
FLoCs explained at the Privacy Sandbox Initiative website
More detailed
FLoC Origin Trial & Clustering – infos from the Chromium project