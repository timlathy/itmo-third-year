module Logic where

import Data.List (intercalate)

data BoolTerm = And [BoolTerm]
              | Or [BoolTerm]
              | Not BoolTerm
              | X Int -- input signal index, starting from 1
              | Q Int -- state signal index, starting from 1
  deriving (Show)

render :: BoolTerm -> String
render (And ts) = render =<< ts
render (Or ts) = intercalate " \\lor " $ render <$> ts
render (Not t) = "\\bar{" ++ render t ++ "}"
render (X i) = "x_" ++ show i
render (Q i) = "Q_" ++ show i

simplify :: BoolTerm -> BoolTerm
simplify (And ts) = And $ simplify <$> filter (not. emptyTerm) ts
simplify (Or ts) = Or $ simplify <$> filter (not. emptyTerm) ts
simplify t = t

emptyTerm :: BoolTerm -> Bool
emptyTerm (And []) = True
emptyTerm (Or []) = True
emptyTerm _ = False
