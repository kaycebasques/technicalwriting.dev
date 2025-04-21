# Chapter 6: RTIC (Real-Time Interrupt-driven Concurrency) Integration

Following our exploration of the [HAL (Hardware Abstraction Layer)](05_hal__hardware_abstraction_layer__.md), this chapter introduces RTIC (Real-Time Interrupt-driven Concurrency), a framework for building safe and efficient concurrent embedded applications on the micro:bit.

## Motivation: Concurrent and Real-Time Applications

Imagine you're building a robot controller using the micro:bit. You need to:

1.  **Control the motors:** This requires generating PWM signals and updating them frequently to adjust the robot's speed and direction.
2.  **Read sensor data:** This involves reading data from sensors like accelerometers, gyroscopes, and distance sensors.
3.  **Process user input:** This requires reading button presses or receiving commands over Bluetooth.

These tasks need to happen concurrently and in real-time. For example, if the robot is about to collide with an obstacle, the motor control needs to react immediately. Handling all these tasks sequentially in a single loop would make the robot sluggish and unresponsive. Traditional multi-threading solutions often introduce data races and other concurrency issues.

RTIC solves this problem by providing a compile-time checked framework for building concurrent and real-time applications. It uses interrupt priorities and static analysis to ensure data race-free execution and predictable timing.

**Use Case:** A robot controller that needs to control motors, read sensor data, and process user input concurrently and in real-time.

## Key Concepts

1.  **Interrupt-Driven:** RTIC applications are built around interrupts. Hardware events (e.g., timer expiration, button press) trigger interrupts, which then execute specific tasks.

2.  **Priority-Based Scheduling:** RTIC uses a priority-based scheduling algorithm. Each task is assigned a priority, and the task with the highest priority that is ready to run will be executed.

3.  **Static Analysis:** RTIC performs static analysis at compile time to ensure that the application is data race-free and that all shared resources are accessed safely.

4.  **Resource Management:** RTIC provides mechanisms for managing shared resources, such as peripherals and memory. Resources can be claimed by tasks, and RTIC ensures that only one task can access a resource at a time.

5.  **Tasks:** Tasks are the fundamental units of execution in an RTIC application. Tasks are defined using the `#[task]` attribute and can be either interrupt-driven or software-triggered.

## Using RTIC

Let's illustrate how to use RTIC with a simple example: blinking an LED using a timer interrupt.

```rust
#![no_std]
#![no_main]

use panic_halt as _;

#[cfg(feature = "v1")]
use microbit::{Board, hal::Timer};

#[cfg(feature = "v2")]
use microbit_v2::{Board, hal::Timer};

use cortex_m_rt::entry;
use rtic::app;

#[app(device = microbit::hal::pac, dispatchers = [SWI0_EGU0])] // Or microbit_v2::hal::pac
mod app {
    use super::*;
    use cortex_m::peripheral::NVIC;
    use embedded_hal::digital::v2::OutputPin;

    #[shared]
    struct Shared {
        led: #[cfg(feature = "v1")] Option<microbit::hal::gpio::P0_21<microbit::hal::gpio::Output<microbit::hal::gpio::PushPull>>>,
        #[cfg(feature = "v2")]
        led: #[cfg(feature = "v2")] Option<microbit_v2::hal::gpio::P1_10<microbit_v2::hal::gpio::Output<microbit_v2::hal::gpio::PushPull>>>,
    }

    #[local]
    struct Local {
        timer: Timer<microbit::hal::pac::TIMER0>, // Or microbit_v2::hal::pac::TIMER0
    }

    #[init]
    fn init(cx: init::Context) -> (Shared, Local, init::Monotonics) {
        let board = Board::new(cx.device. Peripherals::take().unwrap(), cx.core.CorePeripherals::take().unwrap());

        let mut timer = Timer::new(board.TIMER0);
        timer.enable_interrupt();
        timer.start(1_000_000u32); // 1 second

        unsafe {
            NVIC::unmask(microbit::hal::pac::Interrupt::TIMER0); // Or microbit_v2::hal::pac::Interrupt::TIMER0
        }

        #[cfg(feature = "v1")]
        let led = Some(board.display.col1.into_push_pull_output());
        #[cfg(feature = "v2")]
        let led = Some(board.led_matrix.col1.into_push_pull_output());

        (
            Shared { led },
            Local { timer },
            init::Monotonics(),
        )
    }

    #[task(binds = TIMER0, shared = [led], local = [timer])]
    fn blink(cx: blink::Context) {
        static mut TOGGLED: bool = false; // must be static mut

        if *TOGGLED {
            cx.shared.led.lock(|led| {
                if let Some(pin) = led {
                    pin.set_low().unwrap();
                }
            });
            *TOGGLED = false;
        } else {
            cx.shared.led.lock(|led| {
                if let Some(pin) = led {
                    pin.set_high().unwrap();
                }
            });
            *TOGGLED = true;
        }

        cx.local.timer.reset_event();
        cx.local.timer.start(1_000_000u32);
    }
}
```

*Explanation:*

1.  We use the `#[app]` attribute to define an RTIC application. The `device` argument specifies the microcontroller's peripheral access crate (PAC), and the `dispatchers` argument specifies the interrupt dispatchers to use.
2.  The `#[shared]` attribute defines a shared resource, in this case, the `led` pin. Shared resources must be accessed through a lock to prevent data races.
3.  The `#[local]` attribute defines a local resource, in this case, the `timer`. Local resources are only accessible from the task that owns them.
4.  The `#[init]` attribute defines the initialization function. This function is executed once at startup and is responsible for initializing the hardware and setting up the tasks. We initialize the LED pin as an output and start the timer.
5.  The `#[task]` attribute defines a task. The `binds` argument specifies the interrupt that triggers the task, and the `shared` and `local` arguments specify the shared and local resources that the task has access to. In the `blink` task, we toggle the LED's state and reset the timer.
6. We toggle the LED using the shared resource `led`. `lock` prevents race conditions.

*Example Output:* The LED connected to the specified GPIO pin will blink on and off every second.

## Internal Implementation

RTIC uses a combination of static analysis, interrupt priorities, and resource management to ensure safe and efficient concurrent execution. Let's examine the key aspects of the internal implementation.

```mermaid
sequenceDiagram
    participant Hardware
    participant Interrupt Controller (NVIC)
    participant RTIC Scheduler
    participant init()
    participant blink()

    Hardware->>Interrupt Controller (NVIC): Timer expires
    Interrupt Controller (NVIC)->>RTIC Scheduler: Interrupt request (TIMER0)
    RTIC Scheduler->>blink(): Execute blink task
    blink()->>blink(): Toggle LED state (within lock)
    blink()->>Hardware: Set LED pin high/low
    blink()->>Hardware: Reset TIMER0 event
    blink()->>Hardware: Start TIMER0
    blink()->>RTIC Scheduler: Task completes
    RTIC Scheduler->>Interrupt Controller (NVIC): Enable interrupts
```

*Explanation:*

1.  The hardware timer expires, triggering an interrupt.
2.  The interrupt controller (NVIC) receives the interrupt request and signals the RTIC scheduler.
3.  The RTIC scheduler determines the highest-priority task that is ready to run (in this case, the `blink` task) and executes it.
4.  The `blink` task toggles the LED's state (within a lock to prevent data races).
5.  The `blink` task resets the timer event and restarts the timer.
6.  The `blink` task completes, and the RTIC scheduler returns control to the interrupt controller, enabling interrupts.

Let's examine the generated code from the RTIC macro to understand how the resources are managed. While the exact generated code can vary depending on the RTIC version and application configuration, the following snippet illustrates the general principles. (Note: This is pseudo-code, not actual Rust code).

```rust
// (Pseudo-code - Generated by RTIC macro)

static mut LED_RESOURCE: Option<microbit::hal::gpio::P0_21<microbit::hal::gpio::Output<microbit::hal::gpio::PushPull>>> = None; // Or microbit_v2 version
static TIMER0_RESOURCE: Timer<microbit::hal::pac::TIMER0>; // Or microbit_v2 version

fn init() {
    // ... initialization code ...
    LED_RESOURCE = Some(board.display.col1.into_push_pull_output()); // Or microbit_v2 version
    TIMER0_RESOURCE = Timer::new(board.TIMER0);
    // ...
}

fn blink() {
    // ... task code ...
    // Acquire lock on LED resource
    let led = acquire_lock(&LED_RESOURCE);
    // Use LED resource
    led.set_high().unwrap();
    // Release lock on LED resource
    release_lock(&LED_RESOURCE);
    // ...
}
```

*Explanation:*

*   RTIC generates static variables to store the shared resources (`LED_RESOURCE`, `TIMER0_RESOURCE`).
*   The `init()` function initializes these resources.
*   The `blink()` task acquires a lock on the `LED_RESOURCE` before accessing it and releases the lock after it is done. This ensures that only one task can access the LED at a time, preventing data races.

## Contributing Code

Now that you understand RTIC, you're ready to contribute code to the `microbit` project. Here's a potential contribution opportunity:

**Challenge:** Implement a more complex RTIC application that controls the robot motors based on sensor data and user input.

Here's how you might approach this challenge:

1.  **Define tasks for motor control, sensor reading, and user input:** Create separate tasks for each of these functionalities.
2.  **Define shared resources for the motor outputs and sensor data:** Use shared resources to manage access to the motor outputs and sensor data.
3.  **Use interrupt-driven tasks for real-time responsiveness:** Use timer interrupts for motor control and sensor reading to ensure that these tasks are executed at regular intervals. Use button press interrupts for user input to react immediately to user commands.
4.  **Implement the control logic:** Implement the control logic in the motor control task, using the sensor data and user input to adjust the motor speeds and direction.

Remember to follow the existing code style and include comments to explain your code. Test your code thoroughly before submitting a pull request.

## Conclusion

In this chapter, you learned about RTIC, its purpose, and how it enables the development of safe and efficient concurrent embedded applications. You saw how to define tasks, shared resources, and local resources, and how to use RTIC's static analysis to prevent data races.  You also learned how to use interrupt-driven tasks for real-time responsiveness. Finally, you were presented with a challenge to contribute code to the `microbit` project.

There are no more chapters. You are now prepared to contribute to the `microbit` crate.


---

Generated by [AI Codebase Knowledge Builder](https://github.com/The-Pocket/Tutorial-Codebase-Knowledge)