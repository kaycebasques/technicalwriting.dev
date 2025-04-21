# Chapter 2: Board

In the previous chapter, [microbit (crate)](01_microbit__crate__.md), we learned about the `microbit` crate and how it helps us program the micro:bit. Now, let's dive into the `Board` abstraction.

**What is the `Board` and why do we need it?**

Imagine you're playing a video game. You have a character that can perform actions like running, jumping, and interacting with objects. The `Board` in the `microbit` crate is similar to that main character object. It represents the entire micro:bit and provides access to all its features.

Let's say you want to turn on an LED on the micro:bit. Without the `Board`, you'd have to directly interact with the hardware, which is complicated. But with the `Board`, you can simply tell it, "Hey, Board, turn on this LED!".

**The `Board` as a Central Hub**

Think of the `Board` as the central hub that connects you to all the micro:bit's components, like the display, buttons, and sensors. It's a single object that encapsulates everything.

**How to Get the `Board`**

Before we can use the `Board`, we need to get an instance of it.  This is done using the `Board::take()` function.  It's a bit like saying "Give me the micro:bit!".

```rust
use microbit::Board;

fn main() -> ! {
    // Get the board.  The `unwrap()` part handles the case where
    // there isn't a board available (which shouldn't happen on a real micro:bit).
    let board = Board::take().unwrap();

    loop {} // Keep the program running
}
```

**Explanation:**

1.  `use microbit::Board;`: This line imports the `Board` struct from the `microbit` crate.  This makes it possible to use `Board` in our code.
2.  `let board = Board::take().unwrap();`:  This is the crucial line.  `Board::take()` tries to get hold of the micro:bit's resources.  The `.unwrap()` part says "If `Board::take()` fails, panic and stop the program". In most cases this will not fail when the code is executed on an actual micro:bit board.  The result (the `Board` object) is then stored in the `board` variable.
3.  `loop {}`: This creates an infinite loop. This keeps the program running so the micro:bit doesn't stop immediately.

**Accessing the Display**

Now that we have the `Board`, we can access its components.  Let's try accessing the display.  We'll cover the [Display](03_display_.md) in more detail in the next chapter, but for now, let's just see how to get it through the `Board`.

```rust
use microbit::Board;

fn main() -> ! {
    let board = Board::take().unwrap();

    // Get the display from the board
    let mut display = board.display;

    loop {}
}
```

**Explanation:**

1.  `let mut display = board.display;`:  This line retrieves the `display` from the `board` object.  We use `let mut` because we'll likely want to *modify* the display (e.g., to show something on it). The type of `display` is the topic of [Display](03_display_.md).

**Using the Display (A Sneak Peek)**

Although [Display](03_display_.md) dives into this much more, here's a quick example of how you might use the display *after* getting it from the `Board`:

```rust
use microbit::Board;
use embedded_hal::delay::DelayNs; // We need to bring DelayNs into scope to use delay_ms

fn main() -> ! {
    let board = Board::take().unwrap();
    let mut display = board.display;

    // Show a single pixel at (0, 0) (top-left corner)
    display.set_pixel(0, 0, 9); // 9 is maximum brightness

    // Simple delay. `embedded_hal` is covered in [HAL (Hardware Abstraction Layer)](05_hal__hardware_abstraction_layer__pins_.md)
    board.timer.delay_ms(1000);

    loop {}
}
```

**Explanation:**

1. `use embedded_hal::delay::DelayNs;`: This import is needed to make `delay_ms` work. We will cover it in [HAL (Hardware Abstraction Layer)](05_hal__hardware_abstraction_layer__pins_.md)
2.  `display.set_pixel(0, 0, 9);`: This line sets the pixel at coordinates (0, 0) to a brightness of 9 (maximum brightness).  You should see the top-left LED light up!
3.  `board.timer.delay_ms(1000);`:  This line pauses the program for 1000 milliseconds (1 second). This delay prevents the LED from only flashing very briefly. You must also get access to the `board.timer` to use it, which is also a field in the `Board` struct.

**Under the Hood: How `Board::take()` Works**

Let's take a simplified look at what happens when you call `Board::take()`.

```mermaid
sequenceDiagram
    participant User Code
    participant Board::take()
    participant Peripheral Access Crate (PAC)
    participant Board Struct

    User Code->>Board::take(): Request a Board instance
    Board::take()->>Peripheral Access Crate (PAC): Request access to peripherals
    Peripheral Access Crate (PAC)-->>Board::take(): Provides access to peripherals
    Board::take()->>Board Struct: Creates a Board instance with the peripherals
    Board Struct-->>User Code: Returns the Board instance
```

1.  **User Code:** Your program calls `Board::take()`.
2.  **`Board::take()`:** This function is responsible for creating a `Board` instance. It needs access to the micro:bit's hardware components (peripherals).
3.  **Peripheral Access Crate (PAC):** This crate (which we saw as `microbit::hal::pac` in the previous chapter) provides low-level access to the micro:bit's peripherals. `Board::take()` requests access to these peripherals.
4.  **`Board Struct`:**  The `Board` struct is created, containing all the peripherals.
5.  The `Board` instance is returned to your code.

**Internal Implementation (Simplified)**

Here's a very simplified (and incomplete) view of what `Board::take()` might look like inside the `microbit` crate.  *This is for illustrative purposes only and doesn't represent the actual implementation.*

```rust
// Inside the microbit crate (simplified example)

pub struct Board {
    pub display: Display, // The display (covered in the next chapter)
    pub timer: Timer,      // A timer for delays
    // ... other peripherals ...
}

impl Board {
    pub fn take() -> Option<Self> {
        // This is a simplified example!
        // In reality, it involves more complex initialization.

        // First, get access to the peripherals (using the PAC)
        let peripherals = pac::Peripherals::take()?;

        // Create the Display and Timer instances
        let display = Display::new();
        let timer = Timer::new(peripherals.TIMER0); // We need to pass in the Timer peripheral

        // Construct the Board
        let board = Board {
            display,
            timer,
            // ... other peripherals ...
        };

        Some(board)
    }
}
```

**Explanation:**

1.  `pub struct Board { ... }`:  This defines the `Board` struct.  It contains fields for the display, the timer, and other peripherals.
2.  `pub fn take() -> Option<Self> { ... }`: This defines the `take()` function.  It returns an `Option<Self>`, which means it might return a `Board` instance (`Some(board)`) or nothing (`None`) if something goes wrong.
3.  `let peripherals = pac::Peripherals::take()?;`:  This line gets access to the peripherals using the Peripheral Access Crate (PAC).  The `?` operator is a shorthand for error handling.
4. `let timer = Timer::new(peripherals.TIMER0);`: This creates the `Timer` struct.  The timer is created using the peripheral `TIMER0`.
5.  The `Board` instance is constructed, containing the display, the timer and all other peripherals that belong to it.

**In Summary**

The `Board` is your gateway to interacting with the micro:bit's hardware.  It's a single object that represents the entire device and provides access to its various components. By using `Board::take()`, we obtain an instance of the `Board`, allowing us to control the display, buttons, sensors, and more.

In the next chapter, we'll explore the [Display](03_display_.md) in more detail and learn how to show text, draw shapes, and create animations on the micro:bit's LED matrix.


---

Generated by [AI Codebase Knowledge Builder](https://github.com/The-Pocket/Tutorial-Codebase-Knowledge)