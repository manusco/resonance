# Conceptual Model (the objects the user perceives)

> **Objective**: Model the objects a user believes they are working with, and the words for them, before designing the surface. This is the layer between what to build and how it looks.
> **Rule**: One name per concept, everywhere the user meets it. If two screens call the same thing by two names, you have two objects in the user's head and a support ticket waiting to happen.

This is not a database schema and not a wireframe. It sits between `/product` (which decides what to build and why) and `/design` (which crafts the surface). It is also not `architect`'s domain model: that names classes and services for engineers, and it deliberately lets the same word mean different things in different bounded contexts. Here the discipline is the opposite. One user-facing concept gets one name, and the code-facing names defer to it wherever the user can see them.

## Contents

- [1. Objects, not instances](#1-objects-not-instances)
- [2. Attributes and relationships](#2-attributes-and-relationships)
- [3. Lifecycle states](#3-lifecycle-states)
- [4. Verbs: the actions that become CTAs](#4-verbs-the-actions-that-become-ctas)
- [5. The vocabulary dictionary](#5-the-vocabulary-dictionary)
- [6. Object failure modes](#6-object-failure-modes)
- [7. Where this hands off](#7-where-this-hands-off)

## 1. Objects, not instances

Start with a noun harvest: list every thing the user talks about when they describe their work. Then separate the real objects from instances of an object.

- A real object is a thing the user can point at, that has attributes, that things happen to. A Post. An Invoice. A Workspace.
- An instance is one value of an object. "ROAS", "LTV", and "CAC" are not three objects; they are three instances of one object, Metric. Modeling them as separate things multiplies the interface for no reason.
- Test: can you list its attributes and the actions taken on it? If not, it is probably an attribute of another object, or an instance, not an object of its own.

Record the objects the user perceives, not the rows in your database. The two often differ, and the user's model wins on the surface.

## 2. Attributes and relationships

For each object, name its attributes (what it has) and its relationships to other objects, with cardinality and a named role.

- Cardinality: one Workspace has many Projects; a Project belongs to one Workspace.
- Named role: do not just draw a line. Name it. A User *authors* a Post; a Reviewer *approves* a Release. The verb on the relationship is often the missing CTA.
- A relationship the user cannot reach is a broken model (see section 6). If a Post belongs to a Workspace, the user should be able to get from one to the other.

## 3. Lifecycle states

An object's lifecycle states are not the same as an element's visual states. `/design` and the motion reference own hover, focus, loading, empty, and error. This layer owns the states the object moves through in the user's world: Draft, Scheduled, Published, Archived. An Invoice: Draft, Sent, Paid, Overdue, Void.

- Draw the state diagram: which transitions are allowed, and who can trigger each.
- Name the intermediate and terminal states explicitly, including deletion semantics: is Archived reversible? Does Delete destroy or hide? Is history the user can see, or not?
- Missing states are where interfaces break: "what does the screen look like the moment after they click Send, before the server confirms" is a state, and it is usually undesigned.

## 4. Verbs: the actions that become CTAs

The actions a user can take on an object are its verbs, and those verbs become the buttons. Precision here is the difference between a clear interface and a confusing one.

- A generic "Edit" often hides two different real-world operations with different consequences. "Correct the address" (fix a typo) and "Register a change of address" (the customer moved) are not the same act; collapsing them into "Edit" loses the user's intent and the audit trail.
- Name each verb as the user would name the act, not as the system would name the mutation. "Publish", not "Set status to 1".
- The set of verbs on an object is the honest menu. If a verb exists in the model but nowhere on the surface, the object is masked. If a verb appears on the surface with no object behind it, the surface is lying.

## 5. The vocabulary dictionary

Keep one dictionary of the objects, their states, and their verbs, with exactly one name each. That dictionary is authoritative across every place the user meets the word: the UI, the help docs, the onboarding, the emails, and the user-visible API.

- One name per concept. Not "Log in" here and "Sign in" there. Not "Board" in the UI and "Project" in the docs for the same thing.
- The code can name things differently for engineers (`architect` owns that), but wherever a name reaches the user, it defers to this dictionary.
- This is the cheapest reliability win in product design. A consistent vocabulary removes a whole class of "wait, is a Board the same as a Project?" confusion that no amount of visual polish fixes.

## 6. Object failure modes

Four ways a conceptual model breaks, all of which look like surface problems but are not:

- **Shapeshifter**: the same object appears with different attributes or a different name on different screens, so the user cannot tell it is the same thing.
- **Masked**: an object the user thinks in terms of has no first-class place in the interface; it is buried as a field inside another object.
- **Broken**: one object's attributes and actions are scattered across the interface, so the user cannot see it whole.
- **Isolated**: a real relationship exists but the user cannot get from one object to the other; they sit in separate silos.

When a surface audit (`/page-audit`, `/design`) finds confusion, check whether the root is one of these. A vocabulary or object problem cannot be fixed with spacing and color. It has to be fixed here, one layer down.

## 7. Where this hands off

- **From `/product`**: take the validated opportunities and bets and ask "what objects, states, and words does this imply?"
- **To `/design`**: hand over the stabilized object model, its states, and its dictionary, so the surface is built on a settled structure rather than inventing names as it goes.
- **With `architect`**: share the discipline of a ubiquitous language, but stay on the user's side of the line. Where a name is user-visible, this dictionary wins.
- **Checked by `/page-audit`**: the experience audit catches vocabulary drift and shapeshifter objects on the live product, and routes them back here.
