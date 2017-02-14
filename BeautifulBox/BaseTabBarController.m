//
//  BaseTabBarController.m
//  BeautifulBox
//
//  Created by Miles on 17/2/13.
//  Copyright © 2017年 Miles. All rights reserved.
//

#import "BaseTabBarController.h"
#import "BaseNavigationController.h"


#import "HomeViewController.h"
#import "ActivityViewController.h"
#include "ClassifyViewController.h"
#import "ShoppingCartViewController.h"
#include "MineViewController.h"

#define kClassTitle  @"title"
#define kItemImage   @"image"
#define kClassName    @"className"
@interface BaseTabBarController ()

@end

@implementation BaseTabBarController

- (void)viewDidLoad {
    [super viewDidLoad];
    
    
    NSArray  * itemsArray = @[
                              @{kClassName  :@"HomeViewController",
                                kClassTitle :@"首页",
                                kItemImage  :@""},
                              
                              @{kClassName  :@"ActivityViewController",
                                kClassTitle :@"九块九",
                                kItemImage  :@""},
                              
                              @{kClassName  :@"ClassifyViewController",
                                kClassTitle :@"分类",
                                kItemImage  :@""},
                              
                              @{kClassName  :@"ShoppingCartViewController",
                                kClassTitle :@"购物车",
                                kItemImage  :@""},
                              
                              @{kClassName  :@"MineViewController",
                                kClassTitle :@"我的",
                                kItemImage  :@""}
                              ];
    
    
    for (NSDictionary *itemDic in itemsArray) {
        
        UIViewController *controller = [NSClassFromString(itemDic[kClassName]) new];
        BaseNavigationController *nav = [[BaseNavigationController alloc]initWithRootViewController:controller];
//        nav.navigationBar.backgroundColor = [UIColor yellowColor];
        nav.navigationBar.barTintColor = [UIColor redColor];
        UITabBarItem  *tabBarItem  = nav.tabBarItem;
        tabBarItem.title = itemDic[kClassTitle];
        [tabBarItem setTitleTextAttributes:@{NSForegroundColorAttributeName:[UIColor redColor]}forState:UIControlStateSelected];
        tabBarItem.image = [UIImage imageNamed:itemDic[kItemImage]];
    
        
        [self addChildViewController:nav];
    }
}

- (void)didReceiveMemoryWarning {
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}

/*
#pragma mark - Navigation

// In a storyboard-based application, you will often want to do a little preparation before navigation
- (void)prepareForSegue:(UIStoryboardSegue *)segue sender:(id)sender {
    // Get the new view controller using [segue destinationViewController].
    // Pass the selected object to the new view controller.
}
*/

@end
