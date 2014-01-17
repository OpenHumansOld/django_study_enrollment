Django study enrollment
=======================

[This project is in development. The README.md is written to guide development of its features and should be considered aspirational.]

This project is intended to be a stand-alone website that research studies
can use to implement online enrollment process for study participants. Our model
for this comes from the enrollment process used by the Personal Genome Project,
which places strong emphasis on having a highly informed cohort.

To clarify roles in our instructions below: "users" refers to potential study
participants, and "researchers" refers to researchers and other people with
administrative access to user information.

Enrollment processes supported by this software
-----------------------------------------------

This software assumes the following enrollment process:

1. (optional) Eligibility questions: A series of questions is presented to the potential enrollee. If eligibility requirements are met, the user is invited to step 2.
2. The user creates an account by entering their email address.
3. This email address is validated and an account is created.
4. (optional) The user logs in and is presented with an enrollment exam. This may contain multiple modules; once a module is passed it is recorded (i.e. progress is not lost if the user logs out).
5. Once the exam is passed, the user is presented with the study's full consent document.
6. The user electronically signs that document by typing his/her name.
7. (optional) Simple information collection. (e.g. addresses)
8. The user is done and gets emailed a copy of the consent form. The study takes it from here.

Installation
------------

This software is intended to be easily used in cloud infrastructure, eliminating the need for acquiring access to a server locally. Our instructions will cover hosting an instance of this software on Amazon Web Services.

Configuration
-------------

Django's admin interface is used to configure the various aspects of enrollment.
