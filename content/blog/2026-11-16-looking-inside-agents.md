---
title: Looking inside a vision-based agent
summary: What attention patterns and interventions can tell us about behavior—and where interpretation needs care.
date: '2026-11-16'
category: Interpretability
slug: looking-inside-agents
draft: false
---
An agent can appear competent while relying on cues that fail in an unexpected situation. Understanding its behavior requires asking what information it uses and how its internal computations connect to its actions.

## A concrete example

In [Interpretability in Action](https://arxiv.org/abs/2407.12161), my coauthors and I explored VPT, a vision-based Minecraft agent. We analyzed attention patterns and performed interventions to investigate its decision-making.

The agent attended to recent frames and some earlier key frames. We also observed a striking failure: under a particular visual arrangement, a stationary villager in brown clothing beneath green leaves was treated like a tree trunk.

## Observation and intervention

An attention pattern gives a clue about the information available to a model. It does not, by itself, establish a complete causal explanation of an action. Interventions help probe a more specific question: what changes in behavior when a relevant part of the input changes?

This distinction matters when describing an interpretability result. A useful account separates the observed behavior, the intervention, and the proposed explanation. It also makes clear which conclusions are still exploratory.

## Why it matters

For agents that act over time, evaluating task completion is only part of the picture. Studying the mechanisms behind actions can expose brittle associations and help us design more informative evaluations.

The [paper](https://arxiv.org/abs/2407.12161) and [code](https://github.com/KarolisRam/vpt-mi) document the exploratory analysis. This note is a short introduction to that work.
