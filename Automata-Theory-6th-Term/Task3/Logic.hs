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

renderNumericDnf :: BoolTerm -> String
renderNumericDnf (Or ts) = intercalate " \\lor " $ renderNumericDnf <$> ts
renderNumericDnf (And ts) = show $ binToDec $ bit <$> ts
  where
    bit (Not _) = 0
    bit _ = 1
    binToDec (0:bs) = binToDec bs
    binToDec (1:bs) = 2^(length bs) + binToDec bs
    binToDec [] = 0

simplify :: BoolTerm -> BoolTerm
simplify (And ts) = And $ simplify <$> filter (not. emptyTerm) ts
simplify (Or ts) = Or $ simplify <$> filter (not. emptyTerm) ts
simplify t = t

emptyTerm :: BoolTerm -> Bool
emptyTerm (And []) = True
emptyTerm (Or []) = True
emptyTerm _ = False

-- eval :: X encoded -> Q encoded -> term -> 0/1
eval :: [Int] -> [Int] -> BoolTerm -> Int
eval xs _  (X i)    = xs !! (i - 1)
eval _  qs (Q i)    = qs !! (i - 1)
eval xs qs (Not t)  = bitFlip $ eval xs qs t
    where
        bitFlip 1 = 0
        bitFlip 0 = 1
eval xs qs (And ts) = bitAnd $ eval xs qs <$> ts
    where
        bitAnd (0:_)  = 0
        bitAnd (1:[]) = 1
        bitAnd (1:bs) = bitAnd bs
eval xs qs (Or ts)  = bitOr $ eval xs qs <$> ts
    where
        bitOr (1:_)  = 1
        bitOr (0:[]) = 0
        bitOr (0:bs) = bitOr bs
