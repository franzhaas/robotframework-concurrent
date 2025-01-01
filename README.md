# robotframework-concurrent

## Purpose of this repo
This repo serves several tasks.
 - Show the current state of concurrent robot framework executions.
 - propose changes to robot framework
 - base the workshop at robocon about concurrency

## Why reinvent the wheel?
 - [thread enabled fork](https://github.com/test-fullautomation/robotframework-documentation)
 - [robotframework-async-keyword](https://pypi.org/project/robotframework-async-keyword/)
 - async functions have been supported in regular robot framework since 6.1
 - [robotframework-gevent](https://github.com/eldaduzman/robotframework-gevent)
   
many more approaches to run keywords concurrently. All of those I got across had at least one of these drawbacks.:

 - external dependencies
 - single technique approach
 - lack of examples tests and CI
 - Too high code complexity

### The process star approach
This one is straightforward to implement and safe and I have not seen a proposal in the wild.
### The events/task approach
A technique that allows all robot framework features to be used, (only quick ones make sense), from the background threads is a feature not provided by the competing solutions, also the event-based organization appears to be novel.

## Ideas on how to modify the robot framework properly for better concurrency support

### process star
The currently presented solution uses subprocess.Popen, which is ok.
However _IF_ there would be code added to the startup code of the robot framework, we could use multiprocessing.Process, which at least on some platforms uses the Fork call is way more efficient than Popen, and generally the better solution...

An anchor marker could be made available, to be used as a reference point for suites. This would make it easier to debug why a suite was not found, both in hte context of process star, and in regular usage.

### threads and events
Add a checker that warns/fails if a function or method is called from a thread that is not appropriate. This will bring runtime costs, and will not work for functions/methods outside of our control so it would probably be the most useful if it is an optionally enabled feature.

## Advantages and disadvantages
| Tables        | process star           | event/callback/thread  | async functions |
| ------------- |:-------------:| -----:|-----:|
| relation with other concurrency solutions | everything goes | this solution uses threads, don't mix with process-based parallelism (Fork) | |
| limitations on sharing data      | only pickleable, no references, no file objects      |   no limits | |
| performance of data exchange | slower, large data needs to be copied      |    faster, references are possible ||
| synchronisation bugs | not possible      |    avoidable, but possible ||
| order in log is reliable | yes      |    no ||

## Project todo list
 - improve quality control (add mutation testing)
 - get real-world usage examples out
 - add asyncio example
 - add the technique of event/task for function (as oposed to library) keyword libraries.
